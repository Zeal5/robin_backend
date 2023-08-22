from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

from .check_registerd_user import check_registration

@check_registration
async def register_user(update:Update,context:CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"hello {update.message.from_user.full_name}")