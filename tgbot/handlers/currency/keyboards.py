from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                        ReplyKeyboardMarkup, KeyboardButton,
                      )
from tgbot.handlers.currency.static_text import currency_dict

def build_menu (buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def send_currency_keyboard() -> InlineKeyboardMarkup:
    # resize_keyboard=False will make this button appear on half screen (become very large).
    # Likely, it will increase click conversion but may decrease UX quality.
    try:
        buttons = [InlineKeyboardButton(text=c, callback_data=c) for c in currency_dict.values()]
        return InlineKeyboardMarkup(build_menu(buttons, n_cols=5), )
    except Exception as e:
        print(e)


def send_currency_selection_keyboard() ->InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=c, callback_data=c) for c in ('exchange_rate', 'exchange_summ', 'currency_list')]]
    return InlineKeyboardMarkup(buttons)

