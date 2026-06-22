# TG Chat Fetcher

A Python tool for archiving Telegram conversations. Supports multi-target backup, date filtering, and auto-resume.

## Features

- **Multi-Target Backup** — Each target gets its own file (`Backup_Name_ID.txt`)
- **Date Filtering** — Preset ranges (1/6/12 months) or custom start/end dates
- **Auto-Resume** — Saves progress per target, resumes where you left off
- **Entity Caching** — Resolves senders once, faster subsequent runs
- **2FA Support** — Works with Two-Factor Authentication enabled accounts

## Requirements

- Python 3.8+
- Telegram API credentials from [my.telegram.org](https://my.telegram.org/auth)

## Setup

```bash
git clone https://github.com/SirYadav1/tg-chat-fetch.git
cd tg-chat-fetch
pip install -r requirements.txt
```

## Usage

```bash
python fetch_chat.py
```

Follow the interactive prompts to:
1. Enter your API ID, API Hash, and Phone number (saved to `.env` on first run)
2. Select a target (username, ID, or phone number)
3. Choose a date range
4. Wait for the fetch to complete

## Project Structure

```
├── fetch_chat.py      # Main script
├── progress.json      # Auto-generated resume state
├── .env               # Auto-generated credentials (gitignored)
├── .env.example       # Environment template
└── Backup_*.txt       # Generated chat archives
```

## License

MIT
