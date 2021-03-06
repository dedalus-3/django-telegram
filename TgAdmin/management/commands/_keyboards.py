from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from django.conf import settings
from telebot import types

id_admin = settings.ID_ADMIN_FOR_2_BOT
link_bot = settings.TG_SUPPORT_URL

support_callback = CallbackData("ask_support", "user_id", "as_user")


async def keyboard_state_1(link_chat):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="ссылка на чат", url=link_chat))
    return keyboard


async def after_answer_support():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Отвечено', callback_data='after_answer'))
    return keyboard


async def support_keyboard(language, user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Ответить пользователю'
    else:
        contact_id = id_admin
        as_user = 'yes'
        if language == 'en':
            text = 'Write a message to technical support'
        else:
            text = 'Написать сообщение в техподдержку'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text=text, callback_data=support_callback.new(user_id=contact_id, as_user=as_user)))
    return keyboard


async def create_inline_btn(user_id, text_btn1, text_btn2):
    choice = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"{text_btn1}", callback_data=f"yes|{user_id}"),
            InlineKeyboardButton(text=f"{text_btn2}", callback_data=f"no|{user_id}"),
        ],
    ]
    )
    return choice


async def language_inline_btn():
    choice = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский', callback_data="language|ru"),
            InlineKeyboardButton(text='English', callback_data="language|en"),
        ],
    ])
    return choice


async def link(url):
    link = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сделайте заказ', url=url),
        ],
    ])
    return link


async def link_en(url):
    link_en = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Make an order', url=url),
        ],
    ])
    return link_en


def telebot_create_inline_btn(user_id, btn1, btn2):
    choice = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text=f"{btn1}", callback_data=f"yes|{user_id}")
    btn_2 = types.InlineKeyboardButton(text=f"{btn2}", callback_data=f"no|{user_id}")
    choice.add(btn_1, btn_2)
    return choice


def telebot_link(url):
    choice = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text='Сделать заказ', url=url)
    choice.add(btn_1)
    return choice


def telebot_link_en(url):
    choice = types.InlineKeyboardMarkup()
    btn_1  = types.InlineKeyboardButton(text="Make an order", url=url)
    choice.add(btn_1)
    return choice
