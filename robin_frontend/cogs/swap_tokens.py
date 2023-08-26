from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests, json




with open("config.json", "r") as configs_files:
    configs = json.load(configs_files)




async def get_balance(update: Update, context: CallbackContext) -> None:
    headers = {"Content-Type": "application/json"}
    data = {'tg_id': update.effective_user.id}
    response = requests.post(
            configs["backend_url_get_balance"], json=data, headers=headers
        ).text
    
    await update.message.reply_text(f"wallet = {response}")


