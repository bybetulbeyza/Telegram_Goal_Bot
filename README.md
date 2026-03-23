# Baa Bot — Telegram Goal Tracker

A Telegram bot that helps you set and track personal goals.

---

## Features

- Add goals via chat
- List your current goals
- Mark goals as done
- Get motivational messages
- Goals are saved to a local JSON file

---

## Setup

**1. Clone the repo**
```bash
git clone https://bybetulbeyza/Telegram_Goal_Bot.git
cd Telegram_Goal_Bot
```

**2. Install dependencies**
```bash
pip install python-telegram-bot python-dotenv
```

**3. Create a `.env` file**
```
TOKEN=your_telegram_bot_token
BOT_USERNAME=@your_bot_username
```

> Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

**4. Run the bot**
```bash
python Telegram_Goal_Bot.py
```

---

## Commands

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/new_goal` | Add a new goal |
| `/my_goals` | List your goals |
| `/motivate` | Get a motivational message |
| `/help` | Show all commands |

---

## Project Structure

```
Telegram_Goal_Bot/
├── main.py
├── goals.json      # auto-created on first run
├── .env
└── README.md
```

---

## Notes

- Goals are stored locally in `goals.json`
- Each user's goals are stored by their Telegram user ID

---

## Requirements

- Python 3.8+
- python-telegram-bot
- python-dotenv

