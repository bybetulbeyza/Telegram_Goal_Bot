import random
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
load_dotenv() 
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

MOTIVATION_MESSAGES = [
    "🐑Baa! Keep pushing, every step counts! ",
    "Small goals today, big wins tomorrow!",
    "You got this! Mark your goals and shine!",
    "Stay consistent, your streaks are growing!",
]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Baa! 🐑 Hi, I’m your friendly goal-tracking sheep! Let’s add your goals and see those streaks grow!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  help_text = (
      "🐑 Baa! Here’s what I can do:\n\n"
      "/add_goal <goal> - Add a new goal\n"
      "/my_goals - Show your current goals\n"
      "/done <goal> - Mark a goal as completed\n"
      "/help - Show this help message\n\n"
      "/motivate - To see a motivation for you"
      "Let’s grow your streaks and celebrate every small win!"
  )
  await update.message.reply_text(help_text)

async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  msg = random.choice(MOTIVATION_MESSAGES)
  await update.message.reply_text(msg)


def handle_response(text: str) -> str:
  processed: str = text.lower()
  if 'hello' in processed:
    return 'Baa, Ready to help!'
  if 'how are you' in processed:
    return 'living my life, eating grass'
  
  return 'You may try to speak Baa! language maybe, cus thats all i can understand from human tongue Baa!'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message_type: str = update.message.chat.type
  text: str = update.message.text

  if message_type == 'group':
    if BOT_USERNAME in text:
      new_text: str = text.replace(BOT_USERNAME, '').strip()
      response: str = handle_response(new_text)
    else: 
      return
  else:
    response: str = handle_response(text)    

  await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f'Update {update} caused error {context.error}')



if __name__=='__main__': 
  print('Starting bot ...')
  app = Application.builder().token(TOKEN).build()

  #commands
  app.add_handler(CommandHandler('start',start_command)) 
  app.add_handler(CommandHandler('help',help_command)) 
  app.add_handler(CommandHandler('motivate',motivate_command)) 

  #messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))

  #errors
  app.add_error_handler(error)

  #polls the bot
  print('polling the bot ...')
  app.run_polling(poll_interval=1)
