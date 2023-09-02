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

SHOW_BUTTONS, ADD_SECRET, EDIT_BUTTONS = range(3)

with open("config.json", "r") as configs_files:
    configs = json.load(configs_files)


async def editing_wallets(update: Update, context: CallbackContext):
    headers = {"Content-Type": "application/json"}
    query = update.callback_query
    button_choice = query.data
    data = {"tg_id": update.effective_user.id, "button_id": button_choice}
    response = requests.patch(
        configs["backend_url_change_active_wallet"], headers=headers, json=data
    )

    if response.text == "true":
        print(button_choice)
        await show_buttons(update, context)

    if response.status_code == 400:
        await context.bot.send_message(
            update.effective_chat.id, response.json()["detail"]
        )


async def show_buttons(update: Update, context: CallbackContext):
    response = await get_wallets(update.effective_user.id)
    old_wallets_list_message = context.user_data.get("show_wallet_message_id")
    if old_wallets_list_message:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=old_wallets_list_message
        )
    if response.status_code == 200:
        wallets_button_list = []
        # for k, v in enumerate(response.json().values(), 1):
        #     wallets += f"{k} : {v} \n"

        for wallet in json.loads(response.text):
            green_button = ""
            if wallet["wallet_is_active"]:
                green_button = "🟢"
            wallet_button = InlineKeyboardButton(
                f"{wallet['wallet_address']} {green_button} ",
                callback_data=f"{wallet['id']}",
            )
            wallets_button_list.append(wallet_button)

        keyboard = [[i] for i in wallets_button_list]
        reply_markup = InlineKeyboardMarkup(keyboard)
        wallet_buttons_message = await context.bot.send_message(
            update.effective_chat.id,
            "wallets green is active",
            reply_markup=reply_markup,
        )
        context.user_data["show_wallet_message_id"] = wallet_buttons_message.id
        return EDIT_BUTTONS

        # await context.bot.send_message(update.effective_chat.id, wallets)
    elif response.status_code == 400:
        await context.bot.send_message(
            update.effective_chat.id,
            f"*No wallets found*\nTo create new wallet use `/start`",
            parse_mode="Markdown",
        )
    else:
        await context.bot.send_message(
            update.effective_chat.id, f"Something went wrong", parse_mode="Markdown"
        )
    return ConversationHandler.END


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
    print(f"got response {response.status_code} - {response.text}")
    return response


async def got_keys(update: Update, context: CallbackContext) -> int:
    response = "private key and recovery phrase can not start with /"

    if (update.effective_message.text).startswith("/"):
        return ConversationHandler.END

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
        print("clicked")
        await show_buttons(update, context)
        return EDIT_BUTTONS


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

    await update.message.reply_text("Welcome", reply_markup=reply_markup)
    return SHOW_BUTTONS


async def fall_back(update: Update, context: CallbackContext):
    # Call the start command handler to show the buttons again
    # await start_command(update, context)
    command = update.message.text[1:]
    if command == "start":
        await start_command(update, context)
        return ConversationHandler.END

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        SHOW_BUTTONS: [CallbackQueryHandler(button_click)],
        ADD_SECRET: [MessageHandler(filters.TEXT, got_keys)],
        EDIT_BUTTONS: [CallbackQueryHandler(editing_wallets)],
    },
    fallbacks=[
        MessageHandler(filters.ALL, fall_back),
        MessageHandler(filters.Command, fall_back),
    ]
    # per_chat=True,
    # per_user=True,
    # per_message=True,
    ,
    conversation_timeout=7 * 60,
)
