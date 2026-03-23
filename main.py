import random
import json
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

DB_FILE = "goals.json"

MOTIVATION_MESSAGES = [
    "🐑 Baa! Keep pushing, every step counts!",
    "Small goals today, big wins tomorrow!",
    "You got this! Mark your goals and shine!",
    "Stay consistent, your streaks are growing!",
]

def load_goals():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:          # ← DÜZELTME: boş dosya kontrolü
            return {}
        return json.loads(content)

def save_goals(goals_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(goals_data, f, ensure_ascii=False, indent=4)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Baa! 🐑 Hi, I'm your friendly goal-tracking sheep! Let's add your goals and see those streaks grow!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🐑 Baa! Here's what I can do:\n\n"
        "/new_goal - Add a new goal\n"
        "/my_goals - Show your current goals\n"
        "/motivate - Get a motivation message\n"
        "/help - Show this help message\n\n"
        "Let's grow your streaks and celebrate every small win!"
    )
    await update.message.reply_text(help_text)

async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(MOTIVATION_MESSAGES)
    await update.message.reply_text(msg)

async def add_goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_goal"] = True
    await update.message.reply_text("🐑 Baa! What goal do you want to add?")

def handle_response(text: str) -> str:
    processed = text.lower()
    if 'hello' in processed:
        return 'Baa, Ready to help!'
    if 'how are you' in processed:
        return 'Living my life, eating grass 🌿'
    return 'You may try to speak Baa! language maybe, cus thats all I can understand from human tongue. Baa!'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    message_type = update.message.chat.type  # ← DÜZELTME: tanımlanmamış değişken

    if context.user_data.get("waiting_for_goal"):
        all_data = load_goals()
        if user_id not in all_data:
            all_data[user_id] = []
        all_data[user_id].append({"text": text, "done": False})
        save_goals(all_data)
        context.user_data["waiting_for_goal"] = False
        await update.message.reply_text(f"✅ New goal added: {text}")
        return

    # ← DÜZELTME: group chat kontrolü artık çalışıyor
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def list_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    all_data = load_goals()
    goals = all_data.get(user_id, [])  # ← DÜZELTME: all_data'dan oku

    if not goals:
        await update.message.reply_text("🐑 Empty goal list. Baa!")
        return

    msg = "🐑 Your Goals:\n\n"
    for i, g in enumerate(goals, 1):
        status = "✅" if g["done"] else "⬜"
        msg += f"{i}. {status} {g['text']}\n"
    await update.message.reply_text(msg)


if __name__ == '__main__':
    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('motivate', motivate_command))
    app.add_handler(CommandHandler('new_goal', add_goal_command))
    app.add_handler(CommandHandler('my_goals', list_goals))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('Polling the bot ...')
    app.run_polling(poll_interval=1)