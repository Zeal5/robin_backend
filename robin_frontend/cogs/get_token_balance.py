from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext,ConversationHandler

import requests, json

with open("config.json", "r") as configs_files:
    configs = json.load(configs_files)

async def get_token_balance(update: Update, context: CallbackContext):
    headers = {"Content-Type": "application/json"}
    data = {"tg_id": update.effective_user.id}
    response = requests.post(
        configs["backend_url_get_token_balance"], json=data, headers=headers
    ).text

    await update.message.reply_text(f"balance = {response}")