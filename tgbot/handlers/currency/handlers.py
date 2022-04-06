import telegram
from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.currency.static_text import ask_currency, reply_currency
from tgbot.handlers.currency.keyboards import send_currency_keyboard
from tgbot.models import User, Currency

def request_currency(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text=ask_currency,
        reply_markup=send_currency_keyboard()
    )
# обновить метод
def currency_handler(update: Update, context: CallbackContext) -> None:
    # receiving user's location
    u = User.get_user(update, context)
    #lat, lon = update.message.location.latitude, update.message.location.longitude
    #Location.objects.create(user=u, latitude=lat, longitude=lon)
    if data in Currency: json = Currency(data)
    else: currency_request(data)

    curry, result = 'USD', 83.2
    print('currency handler {} {}'.format(curry, result))
    print('callback_query {}'.format(update.callback_query.data))

    update.callback_query.answer(reply_currency.format(curry, result))
    update.callback_query.message.reply_text(reply_currency.format(curry, result))

