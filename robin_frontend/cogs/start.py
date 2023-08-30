from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import json

SHOW_BUTTONS, ADD_SECRET = range(2)

with open("config.json", "r") as configs_files:
    configs = json.load(configs_files)


async def create_new_wallet(tg_id: int, secret: str | bool = False):
    headers = {"Content-Type": "application/json"}
    if not secret:
        data = {"tg_id": tg_id}
        request = requests.post(
            configs["backend_url_create_wallet"], json=data, headers=headers
        )
        # @TODO
        return request.json()
    elif not secret.startswith(r"/"):
        data = {"tg_id": tg_id, "secret": secret}
        request = requests.post(
            configs["backend_url_create_wallet"], json=data, headers=headers
        )
        return request.json()


async def get_wallets(tg_id: int):
    headers = {"Content-Type": "application/json"}
    data = {"tg_id": tg_id}
    response = requests.post(
        configs["backend_url_get_wallets"], json=data, headers=headers
    )
    return response.json()


async def got_keys(update: Update, context: CallbackContext) -> int:
    response = "private key and recovery phrase can not start with /"
    if not (update.effective_message.text).startswith("/"):
        response = await create_new_wallet(
            update.effective_user.id, update.effective_message.text
        )

    intermediate_message_id = context.user_data["intermediate_message_id"]
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=intermediate_message_id
    )
    print(update.effective_chat.id)
    await context.bot.send_message(update.effective_chat.id, response)
    # await context.bot.send_message(update.message.chat_id,update.callback_query.message)
    return ConversationHandler.END


async def button_click(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    button_choice = query.data
    print(query.from_user.id)

    if button_choice == "create_wallet":
        intermediate_message = await context.bot.send_message(
            chat_id=update.effective_chat.id, text="creating new wallet..."
        )
        intermediate_message_id = intermediate_message.id
        request = await create_new_wallet(update.effective_user.id)

        # deleting intermediate message
        await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=intermediate_message_id
        )
        await query.message.reply_text(f"{request}")
        return ConversationHandler.END

    if button_choice == "add_wallet":
        intermediate_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your menmonic or hexadecimal secret key to add wallet",
        )
        context.user_data["intermediate_message_id"] = intermediate_message.id
        return ADD_SECRET
    if button_choice == "get_wallets":
        response = await get_wallets(update.effective_user.id)
        wallets = ""
        for k, v in enumerate(response.values(), 1):
            wallets += f"{k} : {v} \n"

        await context.bot.send_message(update.effective_chat.id, wallets)
        return ConversationHandler.END


async def start_command(update: Update, context: CallbackContext) -> int:
    # Create the two buttons
    button1 = InlineKeyboardButton("Create New Wallet", callback_data="create_wallet")
    button2 = InlineKeyboardButton("Add Wallet", callback_data="add_wallet")
    button3 = InlineKeyboardButton("Get Wallets", callback_data="get_wallets")

    # Combine the two buttons in a single row, each list represents a new row
    keyboard = [
        [
            button1,
            button2,
        ],
        [
            button3,
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Robin HOOD official bot", reply_markup=reply_markup
    )
    return SHOW_BUTTONS


async def fall_back(update: Update, context: CallbackContext):
    await update.message.reply_text("You have to click one of the buttons!")
    # Call the start command handler to show the buttons again
    # await start_command(update, context)
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        SHOW_BUTTONS: [CallbackQueryHandler(button_click)],
        ADD_SECRET: [MessageHandler(filters.TEXT, got_keys)],
    },
    fallbacks=[MessageHandler(filters.ALL, fall_back)]
    # per_chat=True,
    # per_user=True,
    # per_message=True,
)
