from databse.wallet_manager import add_user_keys,get_user_keys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

START, KEYS = range(2)


async def got_keys(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text
    new_user: str = await add_user_keys(update.message.from_user.id, user_input)
    await update.message.reply_text(f"{new_user}")
    return ConversationHandler.END


async def button_click(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    button_choice = query.data

    if button_choice == "button1":
        await query.message.reply_text("creating new wallets please wait...")
        # TODO create a wallet creation function
        wallets = get_user_keys(update.effective_user.id)
        for wallet in wallets:
            await query.message.reply_text(f"{wallet.key_name} : {wallet.key_value}")
           
        return ConversationHandler.END

    if button_choice == "button2":
        await query.message.reply_text("Please enter your keys: ")
        return KEYS


async def start_command(update: Update, context: CallbackContext) -> int:
    # Create the two buttons
    button1 = InlineKeyboardButton("Create Wallet", callback_data="button1")
    button2 = InlineKeyboardButton("Add Wallet", callback_data="button2")

    # Combine the two buttons in a single row, each list represents a new row
    keyboard = [
        [
            button1,
            button2,
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Robin HOOD official bot", reply_markup=reply_markup
    )
    return START


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        START: [CallbackQueryHandler(button_click)],
        KEYS: [MessageHandler(filters.TEXT, got_keys)],
    },
    fallbacks=[],
)
