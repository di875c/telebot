import telegram
from telegram import Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          ConversationHandler, CommandHandler,
                          MessageHandler,Filters)

from tgbot.handlers.currency.static_text import ask_currency, reply_currency, currency_dict
from tgbot.handlers.currency.keyboards import send_currency_keyboard, send_currency_selection_keyboard
from tgbot.models import User
from tgbot.handlers.currency import utils

START_CURR, SELECTION_CUR_MODE, EXCHANGE_RATE, CONVERT_CALCULATOR = range(4)

def currency_start(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text=ask_currency,
        reply_markup=send_currency_selection_keyboard()
    )
    return SELECTION_CUR_MODE


def request_currency(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text=ask_currency,
        reply_markup=send_currency_keyboard()
    )
    return EXCHANGE_RATE


def currency_handler(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    curry = update.callback_query.data
    print(curry)
    try:
        result = utils.rate_currency(curry)
        print(result)
        update.callback_query.message.reply_text(reply_currency.format(curry, result))
    except Exception as e:
        print('эта ошибка приводит к падению','%s' % e)

    return ConversationHandler.END

def convertation_ammount(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text='''example command:
            1231 usd eur 12/03/2021
           <eur> можно не вводить вторую валюту и дату, 
        тогда конвертация будет на сегодня в рубли
           <12/03/2021> дату можно вводить только для 2х валют, 
        без даты курс берется на сегодня
             ''',
        #reply_markup=send_currency_keyboard()
    )
    return CONVERT_CALCULATOR


def converation_calculator(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    text = update.message.text
    result = str(utils.convert(text))
    context.bot.send_message(
        chat_id=u.user_id,
        text = result,
    )
    return ConversationHandler.END


def currency_list_send(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    cur_list = [i + ' : ' + v for i, v in currency_dict.items()]
    result = '\n'.join(cur_list)
    context.bot.send_message(
        chat_id=u.user_id,
        text=result,
    )
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    user = User.get_user(update, context)
    update.message.reply_text(
        text='convertation cancelled'
    )
    return ConversationHandler.END


currency_conversation = ConversationHandler(
    entry_points=[CommandHandler('currency', currency_start)],
    states={
        SELECTION_CUR_MODE: [CallbackQueryHandler(request_currency, pattern = 'exchange_rate' ),
                             CallbackQueryHandler(convertation_ammount, pattern = 'exchange_summ'),
                             CallbackQueryHandler(currency_list_send, pattern = 'currency_list'),
                             CommandHandler('cancel', cancel)
                             ],
        EXCHANGE_RATE: [CallbackQueryHandler(currency_handler),
                        CommandHandler('cancel', cancel)],
        CONVERT_CALCULATOR: [MessageHandler(Filters.text, converation_calculator),
                             CommandHandler('cancel', cancel)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

