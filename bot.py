import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key from env
openai.api_key = os.getenv('OPENAI_API_KEY')

# Telegram bot token from env
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Gmoney$ AI Bot! Send me a message.')

def echo(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    # Call OpenAI API for response
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_text,
            max_tokens=50
        )
        bot_reply = response.choices[0].text.strip()
    except Exception as e:
        bot_reply = "Sorry, I couldn't process your request."

    update.message.reply_text(bot_reply)

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
