from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.handlers.currency.static_text import currency_dict

def send_currency_keyboard() -> InlineKeyboardMarkup:
    # resize_keyboard=False will make this button appear on half screen (become very large).
    # Likely, it will increase click conversion but may decrease UX quality.
    buttons = [[InlineKeyboardButton(text=c, callback_data=c) for c in currency_dict.values()]]
    return InlineKeyboardMarkup(buttons, row_width=4)