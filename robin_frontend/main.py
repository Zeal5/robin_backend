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
from cogs.buy_tokens_with_eth import buy_tokens_with_eth_convo_handler
load_dotenv()
token = os.getenv("TOKEN")




def main():
    print("bot started")
    app = Application.builder().token(token).build()
    # conv_handler.fallbacks.append(CommandHandler('something', command_handler))
    app.add_handler(conv_handler,1)
    app.add_handler(buy_tokens_with_eth_convo_handler,2)
    # app.add_handler(CommandHandler("token_balance",get_token_balance),2)
    # app.add_handler(MessageHandler(filters.Command,command_handler))


    # polling
    app.run_polling(3, allowed_updates=Update.ALL_TYPES)

"""
start - startr setup
buy_tokens_with_eth - token address , amount eth
token_balance - get token balance

"""


if __name__ == "__main__":
    main()
