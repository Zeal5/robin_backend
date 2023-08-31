from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests, json




with open("config.json", "r") as configs_files:
    configs = json.load(configs_files)




async def swap_token(update: Update, context: CallbackContext) -> None:
    headers = {"Content-Type": "application/json"}
    data = {'tg_id': update.effective_user.id}
    response = requests.post(
            configs["backend_url_buy"], json=data, headers=headers
        ).text
    
    await update.message.reply_text(f"wallet = {response}")
    # message = update.effective_message.text.split(" ")[1:]
    # print(len(message)) 

    # print(message)




async def get_token_balance(update:Update, context:CallbackContext) :
    headers = {"Content-Type": "application/json"}
    data = {'tg_id': update.effective_user.id}
    response = requests.post(
            configs["backend_url_get_token_balance"], json=data, headers=headers
        ).text
    
    await update.message.reply_text(f"balance = {response}")
