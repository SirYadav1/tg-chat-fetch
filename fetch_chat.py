import os
import json
import asyncio
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import User
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich import print as rprint

# Initialize console for pretty printing
console = Console()

# Configuration
SESSION_NAME = 'tg_fetcher_session'
PROGRESS_FILE = 'progress.json'
ENV_FILE = '.env'

# Load environment variables if available
load_dotenv()

def load_progress(target_id):
    """Retrieves the last saved message ID for a specific target."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                data = json.load(f)
                return data.get(str(target_id))
        except (json.JSONDecodeError, Exception):
            return None
    return None

def save_progress(target_id, message_id):
    """Saves the current offset to resume fetching later."""
    data = {}
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                data = json.load(f)
        except Exception:
            pass
    
    data[str(target_id)] = message_id
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def save_env_credentials(api_id, api_hash, phone):
    """Automatically saves credentials to .env file."""
    env_content = f"API_ID={api_id}\nAPI_HASH={api_hash}\nPHONE={phone}\n"
    with open(ENV_FILE, 'w') as f:
        f.write(env_content)
    rprint("[dim green]✔ Credentials auto-saved to .env[/dim green]")

def setup_header():
    """Displays a professional application header."""
    console.clear()
    console.print(Panel.fit(
        " [bold cyan]Telegram Chat Fetcher Pro[/bold cyan] \n[dim]A robust tool for archiving conversations[/dim]",
        border_style="blue"
    ))

async def get_date_limit():
    """Prompts user for a date range filter (Start and End)."""
    rprint("\n[bold cyan]Select Date Range:[/bold cyan]")
    rprint("1. [bold]Last 1 Month[/bold]")
    rprint("2. [bold]Last 6 Months[/bold]")
    rprint("3. [bold]Last 1 Year[/bold]")
    rprint("4. [bold]Custom Range[/bold] [dim](Specify Start & End)[/dim]")
    rprint("5. [bold]All Messages[/bold]")
    
    choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"], default="5")
    
    now = datetime.now()
    if choice == "1":
        return now - timedelta(days=30), now
    elif choice == "2":
        return now - timedelta(days=182), now
    elif choice == "3":
        return now - timedelta(days=365), now
    elif choice == "4":
        rprint("[yellow]Format example: 2024-01-01[/yellow]")
        start_str = Prompt.ask("Enter Start Date [dim](Earlier date)[/dim]")
        end_str = Prompt.ask("Enter End Date [dim](Later date, usually today's date)[/dim]", default=now.strftime('%Y-%m-%d'))
        try:
            start_date = datetime.strptime(start_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_str, '%Y-%m-%d')
            
            # Auto-swap if user put them in wrong order
            if start_date > end_date:
                start_date, end_date = end_date, start_date
                rprint("[yellow]ℹ Noticed dates were reversed. Swapped them for you.[/yellow]")

            # Add time to end_date to include the full day
            end_date = end_date.replace(hour=23, minute=59, second=59)
            return start_date, end_date
        except ValueError:
            rprint("[red]Invalid date format. Using 'All Messages' instead.[/red]")
            return None, None
    return None, None

async def main():
    setup_header()
    
    # Try to get credentials from .env first
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE')

    credentials_needed = False
    if not api_id or not api_hash:
        credentials_needed = True
        rprint("[yellow]Notice: API credentials not found in environment variables.[/yellow]")
        rprint("[dim]Tip: We will save these for you automatically once you login.[/dim]\n")
        
        if not api_id:
            api_id = Prompt.ask("[bold]Enter your API ID[/bold]")
        if not api_hash:
            api_hash = Prompt.ask("[bold]Enter your API Hash[/bold]")
    
    if not phone:
        phone = Prompt.ask("[bold]Enter your Phone Number[/bold] [dim](with country code, e.g., +91...)[/dim]")

    if not all([api_id, api_hash, phone]):
        rprint("[red]Error: All credentials (API ID, Hash, and Phone) are required.[/red]")
        return

    client = TelegramClient(SESSION_NAME, int(api_id), api_hash)
    
    try:
        with console.status("[bold blue]Connecting to Telegram...") as status:
            await client.connect()
        
        if not await client.is_user_authorized():
            rprint("[yellow]Notice: Authorization required.[/yellow]")
            try:
                with console.status("[bold blue]Sending OTP...") as status:
                    await client.send_code_request(phone)
                
                otp_code = Prompt.ask("[bold green]Enter the Login Code received on Telegram[/bold green]")
                try:
                    await client.sign_in(phone, otp_code)
                except Exception as e:
                    from telethon.errors import SessionPasswordNeededError
                    if isinstance(e, SessionPasswordNeededError):
                        password = Prompt.ask("[bold green]Enter your 2FA Password[/bold green]", password=True)
                        await client.sign_in(password=password)
                    else:
                        raise e
            except Exception as e:
                rprint(f"[red]Authentication failed:[/red] {e}")
                return

        # Auto-save credentials if they were entered manually
        if credentials_needed:
            save_env_credentials(api_id, api_hash, phone)

        rprint("[green]✔ Authentication successful![/green]\n")
        
        target = Prompt.ask("[bold]Target User (Username, ID, or Phone)[/bold]")
        
        with console.status("[bold magenta]Locating target...") as status:
            try:
                if target.replace('-', '').isdigit():
                    entity = await client.get_entity(int(target))
                else:
                    entity = await client.get_entity(target)
            except Exception as e:
                rprint(f"[red]Failed to find target:[/red] {e}")
                rprint("\n[yellow]💡 Tip:[/yellow] If you are using a new account/session:")
                rprint("1. Try using the [bold]Username[/bold] (e.g., @username) instead of ID.")
                rprint("2. Make sure you have a [bold]chat history[/bold] or shared group with this person.")
                rprint("3. Try sending them a [bold]'Hi'[/bold] first from your Telegram app.")
                return

        target_id = entity.id
        name = f"{getattr(entity, 'first_name', '')} {getattr(entity, 'last_name', '')}".strip() or getattr(entity, 'title', 'Unknown')
        # Sanitize name for filename
        clean_name = "".join([c for c in name if c.isalnum() or c in (' ', '_')]).replace(' ', '_')
        target_filename = f"Backup_{clean_name}_{target_id}.txt"
        
        rprint(Panel(f"Target: [bold]{name}[/bold]\nID: [dim]{target_id}[/dim]\nFile: [bold cyan]{target_filename}[/bold cyan]", border_style="green", expand=False))

        # Date filtering logic
        start_date, end_date = await get_date_limit()
        
        offset_id = load_progress(target_id) or 0
        
        if start_date and end_date:
            rprint(f"[cyan]ℹ Fetching messages between {start_date.date()} and {end_date.date()}[/cyan]")
            offset_id = 0 # Start fresh for specific ranges
        elif offset_id:
            rprint(f"[cyan]ℹ Resuming from message ID: {offset_id}[/cyan]")
        
        rprint("\n[bold]Starting fetch...[/bold] [dim](Press Ctrl+C to stop)[/dim]\n")

        count = 0
        start_time = time.time()
        sender_cache = {}
        
        first_msg_time = None
        last_msg_time = None

        with open(target_filename, 'a', encoding='utf-8') as f:
            async for message in client.iter_messages(entity, offset_id=offset_id, offset_date=end_date, reverse=False):
                if start_date and message.date.replace(tzinfo=None) < start_date:
                    rprint(f"\n[yellow]Reached limit: Messages are now older than {start_date.date()}.[/yellow]")
                    break

                save_progress(target_id, message.id)
                
                if message.text and not any([message.sticker, message.video, message.voice]):
                    m_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
                    if not first_msg_time:
                        first_msg_time = m_time
                    last_msg_time = m_time
                    
                    sender_id = message.sender_id
                    if sender_id not in sender_cache:
                        sender = await message.get_sender()
                        if sender:
                            if isinstance(sender, User):
                                sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
                            else:
                                sender_name = getattr(sender, 'title', 'Unknown')
                        else:
                            sender_name = "System"
                        sender_cache[sender_id] = sender_name
                    else:
                        sender_name = sender_cache[sender_id]

                    timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
                    clean_text = message.text.replace('\n', ' ')
                    
                    line = f"[{timestamp}] [{sender_name}]: {message.text}\n"
                    f.write(line)
                    f.flush()
                    
                    count += 1
                    rprint(f"[dim]{timestamp}[/dim] [bold blue]{sender_name}:[/bold blue] {clean_text[:60]}...")

        end_time = time.time()
        total_time = end_time - start_time
        speed = count / total_time if total_time > 0 else count

        # Finishing Summary
        rprint("\n", Panel.fit(
            f"[bold green]Fetch Complete![/bold green]\n\n"
            f"📅 [bold]Range:[/bold] {last_msg_time or 'N/A'} [dim]to[/dim] {first_msg_time or 'N/A'}\n"
            f"📥 [bold]Total Messages:[/bold] {count}\n"
            f"⏱ [bold]Time Taken:[/bold] {total_time:.2f} seconds\n"
            f"⚡ [bold]Speed:[/bold] {speed:.2f} msgs/sec\n"
            f"📄 [bold]File:[/bold] {target_filename}",
            title="Session Summary",
            border_style="green"
        ))

    except KeyboardInterrupt:
        rprint("\n[yellow]Stopped by user. Progress has been saved.[/yellow]")
    except Exception as e:
        rprint(f"\n[red]An unexpected error occurred:[/red] {e}")
    finally:
        await client.disconnect()
        rprint("[dim]Session closed.[/dim]")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except EOFError:
        pass
