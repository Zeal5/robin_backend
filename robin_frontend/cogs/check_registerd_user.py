from functools import wraps
from telegram import Update
from telegram.ext import  CallbackContext


REGISTERED_USERS = [6115506805]

def check_registration(func):
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        print(user_id)
        if user_id in REGISTERED_USERS:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("You need to register first. Please use /start to register.")
    return wrapper