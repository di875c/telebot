import telegram
from telegram import Update
from telegram.ext import (Updater, Filters,CallbackContext, \
    CommandHandler, MessageHandler, \
    CallbackQueryHandler, ConversationHandler)

from tgbot.handlers.location.static_text import *
from tgbot.handlers.location.keyboards import send_location_keyboard
from tgbot.models import User, Location
from telegram import Bot
from dtb.settings import TELEGRAM_TOKEN

START, LOCATION_F, DESCRIPTION_F, PHOTO_F = range(4)
# USER_STATE = defaultdict(lambda : START)
location=Location()


def ask_for_location(update: Update, context: CallbackContext) -> None:
    """ Entered /ask_location command"""
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text=share_location,
        reply_markup=send_location_keyboard()
    )


def location_handler(update: Update, context: CallbackContext) -> None:
    # receiving user's location
    u = User.get_user(update, context)
    lat, lon = update.message.location.latitude, update.message.location.longitude
    Location.objects.create(user=u, latitude=lat, longitude=lon)

    update.message.reply_text(
        thanks_for_location,
        reply_markup=telegram.ReplyKeyboardRemove(),
    )


def add_place(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    context.bot.send_message(
        chat_id=u.user_id,
        text=request_location
    )
    return LOCATION_F

def add_some_location(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    location.user = u
    location.latitude, location.longitude = update.message.location.latitude, update.message.location.longitude
    context.bot.send_message(
        chat_id = u.user_id,
        text = request_location_description
    )
    return DESCRIPTION_F


def add_location_description(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    _description = update.message.text
    location.description = _description
    Location.objects.create(
        user=u,
        latitude=location.latitude,
        longitude=location.longitude,
        description=location.description,
        # image=file,
    )
    context.bot.send_message(
        chat_id = u.user_id,
        text = request_location_end
    )
    return ConversationHandler.END


# def add_location_photo(update: Update, context: CallbackContext) -> None:
#     u = User.get_user(update, context)
#     # пока не работает сохранение фотографий в базу данных
#     # _photo = update.message.photo[-1]
#     bot = Bot(TELEGRAM_TOKEN)
#     file_info = bot.getFile(update.message.photo[-1].file_id)
#
#     # _photo = update.message.document
#     # location.image = requests.get(_photo.file_path)
#     print('последний принт перед сохраненинм',
#           location.user_id, location.longitude, location.description, file_info, sep='\n')
#     try:
#         # file = bot.download_file(file_info.file_path)
#
#         # print(type(file))
#         Location.objects.create(
#             user=u,
#             latitude=location.latitude,
#             longitude=location.longitude,
#             description=location.description,
#             # image=file,
#         )
#     except Exception as e:
#         print('эта ошибка приводит к падению','%s' % type(e))
#     context.bot.send_message(
#         chat_id = u.user_id,
#         text = request_location_end,
#         photo = file
#     )
#     return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    user = User.get_user(update, context)
    update.message.reply_text(
        text=cancel_location_end
    )
    return ConversationHandler.END


def list_location(update: Update, context: CallbackContext):
    user = User.get_user(update, context)
    if Location.objects.filter(user=user):
        for loc in list(Location.objects.filter(user=user).order_by('-created_at')[:10:]):
            update.message.reply_text(
                text=str(loc)
            )
            update.message.reply_location(latitude=loc.latitude, longitude=loc.longitude)
    else:
        update.message.reply_text(
            text=no_location
        )


def reset_location(update: Update, context: CallbackContext):
    user = User.get_user(update, context)
    [loc.delete() for loc in Location.objects.filter(user=user).order_by('-created_at')]


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_place)],
    states={
        LOCATION_F: [MessageHandler(Filters.location, add_some_location)],
        DESCRIPTION_F: [MessageHandler(Filters.text, add_location_description)],
        # PHOTO_F: [MessageHandler(Filters.photo, add_location_photo)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
