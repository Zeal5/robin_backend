import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)

# import custom pakages
from cogs.start import start_command, got_keys, conv_handler

load_dotenv()
token = os.getenv("TOKEN")


def main():
    print("bot started")
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)

    # polling
    app.run_polling(3, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
