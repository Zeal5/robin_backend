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
from cogs.main_menu import main_menu_convo_handler
from cogs.wallet_cogs.wallet_manager import wallet_manager_convo_handler 
from cogs.buy_tokens_with_eth import buy_tokens_with_eth_convo_handler
from cogs.get_token_balance import get_token_balance
load_dotenv()
token = os.getenv("TOKEN")




def main():
    print("bot started")
    app = Application.builder().token(token).build()
    app.add_handler(main_menu_convo_handler,5)
    app.add_handler(wallet_manager_convo_handler,4)
    app.add_handler(buy_tokens_with_eth_convo_handler,2)
    app.add_handler(CommandHandler("token_balance",get_token_balance),3)
    # app.add_handler(MessageHandler(filters.Command,command_handler))


    # polling
    app.run_polling(0, allowed_updates=Update.ALL_TYPES)

"""
main_menu - Main menu for bot
manage_wallets - create new wallet, add wallet, check all wallets
buy_tokens_with_eth - token address , amount eth
token_balance - get token balance

"""


if __name__ == "__main__":
    main()
