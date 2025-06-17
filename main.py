import os
import json
import logging
import openai
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

def load_memory(user_id):
    filename = f"memory/{user_id}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_memory(user_id, history):
    os.makedirs("memory", exist_ok=True)
    with open(f"memory/{user_id}.json", "w") as f:
        json.dump(history, f)

def reply(update, context):
    user_id = str(update.effective_user.id)
    message = update.message.text
    logging.info(f"📩 Message from {user_id}: {message}")

    history = load_memory(user_id)
    history.append({"role": "user", "content": message})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"⚠️ Error: {e}"

    update.message.reply_text(reply_text)
    logging.info(f"🤖 Reply to {user_id}: {reply_text}")
    history.append({"role": "assistant", "content": reply_text})
    save_memory(user_id, history)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    logging.info("✅ PocketPalAI with memory is running...")
    updater.idle()

if __name__ == "__main__":
    main()
