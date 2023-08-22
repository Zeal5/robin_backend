import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater ,
    Application,
    CommandHandler,
    MessageHandler ,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)

# import custom pakages
from cogs.start import start_command,got_keys, conv_handler
from cogs.register_user import register_user
load_dotenv()
token = os.getenv("TOKEN")

def main():
    print("bot started")
    app = Application.builder().token(token).build()

    # /start handler
    # app.add_handler(CommandHandler("start", start_command))
    # app.add_handler(CallbackQueryHandler(button_click))
    # app.add_handler(MessageHandler(filters.TEXT & filters.Regex('^aaa$') & ~filters.COMMAND, not_got_keys))
    # app.add_handler(MessageHandler(filters.TEXT & filters.Regex('.{6,}') & ~filters.COMMAND, got_keys))
    app.add_handler(conv_handler)

    # /register handler
    app.add_handler(CommandHandler("register", register_user))

    # polling
    app.run_polling(3, allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
