# PocketPalAI Bot 🤖

A Telegram bot powered by ChatGPT with long-term memory per user, hosted on Railway.

## Features
- Saves memory per Telegram user
- Simple config via environment variables
- Deploys 24/7 with Railway

## Setup

1. Add your `TELEGRAM_TOKEN` and `OPENAI_API_KEY` to Railway variables
2. Set the start command to:

```bash
python3 main.py
