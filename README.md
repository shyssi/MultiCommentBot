# MultiCommentBot

Telegram bot that automatically comments on posts forwarded from specified channels.

A Telegram bot that automatically comments on posts sent from specified channels. You can add several blocks with information about channels and the bot will comment on posts in these channels.

## Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/shyssi/MultiCommentBot.git
cd MultiCommentBot
```
# Install dependencies
```bash
pip install -r requirements.txt
```
# Configuration
Create .env file (or use existing tokens.env):
```
TOKEN=your_bot_token_from_BotFather
```

# Edit config.json:
- Add channel IDs as keys.
- Configure caption, image, chat link, etc.

Example structure is already in the file.

Place your images in the static/ folder.

## Run the bot
```bash
python bot.py
```
## Commands
```
/status — show bot status (admin only)
```
