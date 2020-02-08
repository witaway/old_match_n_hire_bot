from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


###
markup_firststart = types.ReplyKeyboardMarkup(True, True)
markup_firststart.row_width = 2
markup_firststart.add(InlineKeyboardButton("Ищу работу", callback_data="cb_work"),
                      InlineKeyboardButton("Ищу работников", callback_data="cb_workers"))

###Новый старт
markup_newstart = types.ReplyKeyboardMarkup()
markup_newstart.row('Да.')

###Оценка
markup_matching = types.ReplyKeyboardMarkup(True, True)
markup_matching.row_width = 2
markup_matching.add(InlineKeyboardButton("Да.", callback_data="cb_yes"),
                    InlineKeyboardButton("Нет.", callback_data="cb_no"))
markup_matching.add(InlineKeyboardButton("Изменить анкету.", callback_data="cb_change"))

###Аватарка
markup_avapic = types.ReplyKeyboardMarkup(True, True)
markup_avapic.row_width = 1
markup_avapic.add(InlineKeyboardButton("Не хочу загружать фотографию.", callback_data="cb_no"))
