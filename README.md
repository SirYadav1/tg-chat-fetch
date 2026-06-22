# TG Chat Fetcher

A Python tool for archiving Telegram conversations with support for multi-target backup, date filtering, and auto-resume.

## Features

| Feature | Description |
|---------|-------------|
| Multi-Target Backup | Each target gets its own file (`Backup_Name_ID.txt`) |
| Date Filtering | Preset ranges (1/6/12 months) or custom start/end dates |
| Auto-Resume | Saves progress per target, resumes where you left off |
| Entity Caching | Resolves senders once, faster subsequent runs |
| 2FA Support | Works with Two-Factor Authentication enabled accounts |

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

Follow the interactive prompts to enter your credentials, select a target, and choose a date range. Credentials are auto-saved to `.env` on first run.

## Project Structure

```
├── fetch_chat.py      # Main script
├── progress.json      # Auto-generated resume state
├── .env               # Auto-generated credentials (gitignored)
├── .env.example       # Environment template
└── Backup_*.txt       # Generated chat archives
```
