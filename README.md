# 📡 TG Chat Fetcher Pro
> **The Ultimate Telegram Archiving Suite** — High-speed, Resilient, and User-Centric.

[![Python Version](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/Engine-Telethon-0088CC?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/LonamiWebs/Telethon)
[![Architecture](https://img.shields.io/badge/Architecture-Asynchronous-8E44AD?style=for-the-badge)](https://asyncio.readthedocs.io/)
[![UI](https://img.shields.io/badge/Interface-Rich_CLI-E67E22?style=for-the-badge)](https://github.com/Textualize/rich)

**TG Chat Fetcher Pro** is a high-grade terminal application designed for power users who demand precision, speed, and reliability when archiving Telegram conversations. Unlike basic scripts, this suite offers a full-featured environment with multi-target support and intelligent state management.

---

## 🚀 Key Advantages

| Feature | Description | Benefit |
| :--- | :--- | :--- |
| **📂 Multi-Target** | Unique files per user (`Backup_Name_ID.txt`) | Organized & Non-destructive |
| **⚡ Entity Caching** | Reduces API calls by resolving senders once | 300% Speed improvement |
| **📅 Date Filtering** | Strict preset & custom time-range selection | Target precise data |
| **🔄 Auto-Resume** | Independent state tracking per target | Pick up exactly where you left |
| **🔐 Auto-Auth** | Seamless `.env` & session management | Zero repeatable login overhead |

---

## 🛠️ Core Features in Detail

### 📂 Multi-Target Backup System
Stop worrying about overwriting your data. Every target (User, Group, or Bot) gets its own dedicated archive file named dynamically using their display name and unique Telegram ID.

### 📅 Advanced Date Range Engine
Filter messages with surgical precision. 
- **Presets**: 1 Month, 6 Months, 1 Year.
- **Custom**: Define exact Start and End dates. 
- **Smart Logic**: Automatically corrects date ordering if entered incorrectly.

### 🛡️ Enterprise-Grade Security
Your credentials stay where they belong—on your machine.
- **Auto-Persistence**: Manually entered `API_ID` and `API_HASH` are automatically saved to a local `.env` file.
- **2FA Ready**: Full support for accounts with Two-Factor Authentication.
- **Session Locking**: Standard `.session` files ensure secure, persistent connections.

---

## 📦 Installation & Setup

### 1. Requirements
- **Python 3.8+**
- Telegram API Credentials from [my.telegram.org](https://my.telegram.org/auth).

### 2. Deployment
```bash
# Clone the repository
git clone https://github.com/yourusername/tg-chat-fwtch.git

# Navigate to project
cd tg-chat-fwtch

# Install optimized dependencies
pip install -r requirements.txt
```

### 3. Execution
Launch the engine and follow the pro-grade interactive CLI:
```bash
python fetch_chat.py
```

---

## 📂 Project Governance
```text
.
├── fetch_chat.py      # Core Execution Engine
├── progress.json      # Per-target State Tracking
├── .env               # (Auto-generated) Secured Credentials
├── .env.example       # Environment Template
└── Backup_*.txt       # Individual Chat Archives
```

---

## 🤝 Contribution
Contributions are the heart of open source. Whether it's adding features, fixing bugs, or improving documentation, your help is welcome!
1. Fork the repo.
2. Create your branch.
3. Submit a PR.

---
> [!IMPORTANT]
> **Disclaimer**: This tool is designed for authorized personal backup and compliance purposes. Always respect privacy laws and Telegram's Terms of Service.

*Copyright © 2026 - Created with ❤️ for the Developer Community.*
