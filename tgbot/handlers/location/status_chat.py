from telegram import Update
from collections import defaultdict
from tgbot.models import User, Location
from telegram.ext import CallbackContext

def get_state (update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    return USER_STATE(u.user_id)

def update_state (update: Update, context: CallbackContext, state):
    u = User.get_user(update, context)
    USER_STATE[update.message.chat_id] = state
