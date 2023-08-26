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
from cogs.swap_tokens import get_balance
load_dotenv()
token = os.getenv("TOKEN")


def main():
    print("bot started")
    app = Application.builder().token(token).build()
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("balance", get_balance))

    # polling
    app.run_polling(3, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
