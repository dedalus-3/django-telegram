import datetime
import time

import telebot
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from telebot import apihelper

from TgAdmin.constants import Const
from TgAdmin.models import Chat, Data

from ._keyboards import telebot_create_inline_btn, telebot_link, telebot_link_en


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(token=settings.BOT_TOKEN)

        def user_name(user) -> str:
            if user.username:
                return f'Добро пожаловать <a href="tg://user?id={user.iduser}">{user.username}</a>!'
            elif user.fullname:
                return f'Добро пожаловать <a href="tg://user?id={user.iduser}">{user.fullname}</a>!'
            else:
                return f'Добро пожаловать <a href="tg://user?id={user.iduser}">пользователь</a>!'

        def user_name_en(user) -> str:
            if user.username:
                return f'Welcome <a href="tg://user?id={user.iduser}">{user.username}</a>!'
            elif user.fullname:
                return f'Welcome <a href="tg://user?id={user.iduser}">{user.fullname}</a>!'
            else:
                return f'Welcome <a href="tg://user?id={user.iduser}">user</a>!'

        def user_name_link(user) -> str:
            if user.username:
                return f'Уважаемый <a href="tg://user?id={user.iduser}">{user.username}</a>!'
            elif user.fullname:
                return f'Уважаемый <a href="tg://user?id={user.iduser}">{user.fullname}</a>!'
            else:
                return f'Уважаемый <a href="tg://user?id={user.iduser}">пользователь</a>!'

        def user_name_link_en(user) -> str:
            if user.username:
                return f'Dear <a href="tg://user?id={user.iduser}">{user.username}</a>!'
            elif user.fullname:
                return f'Dear <a href="tg://user?id={user.iduser}">{user.fullname}</a>!'
            else:
                return f'Dear <a href="tg://user?id={user.iduser}">user</a>!'

        text = Data.objects.get().text_before_btn
        text_en = Data.objects.get().text_before_btn_en
        for chat in Chat.objects.all():
            if chat.language == 'en':
                for i in chat.users.filter(Q(state='1') | Q(state='2')):
                    difference = datetime.datetime.now().date() - i.date_joined.date()
                    if difference.days != 0 & difference.days % 3 == 0:
                        try:
                            if i.state == '1':
                                keyboard = telebot_create_inline_btn(i.iduser, Data.objects.get().btn1_en,
                                                                     Data.objects.get().btn2_en)
                                if not Data.objects.first().image:
                                    bot.send_message(chat_id=chat.chat_id, text=f'{user_name_en(i)}\n{text_en}',
                                                     reply_markup=keyboard, parse_mode='HTML')
                                else:
                                    bot.send_photo(chat_id=chat.chat_id, photo=Data.objects.first().image,
                                                   caption=f'{user_name_en(i)}\n{text_en}', reply_markup=keyboard,
                                                   parse_mode='HTML')
                            else:
                                # chat_url_link_db = chat.url_link
                                # for e in Const.LINK:
                                #    if chat_url_link_db == e[0]:
                                #        chat_url_link = e[1]
                                # keyboard_link = telebot_link_en(chat_url_link)
                                keyboard_link = telebot_link_en(
                                    settings.LINK_MAILING_EN_GROUP)
                                bot.send_message(chat_id=chat.chat_id,
                                                 text=f'{user_name_link_en(i)}\n'
                                                      f'You clicked <b>YES(agreed with our conditions '
                                                      f'https://t.me/realengaforIG) click the button for making an '
                                                      f'order</b>',
                                                 reply_markup=keyboard_link, parse_mode='HTML')
                        except apihelper.ApiException as err:
                            time.sleep(int(str(err).split(' ')[-1]))
                    # elif i.date_joined.date() + datetime.timedelta(days=7) == datetime.datetime.now().date():
                    #    try:
                    #        bot.kick_chat_member(chat.chat_id, i.iduser)
                    #        user = Users.objects.get(iduser=i.iduser)
                    #        user.state = '3'
                    #        user.save()
                    #   except apihelper.ApiException:
                    #        pass
                    else:
                        continue
            else:
                for i in chat.users.filter(Q(state='1') | Q(state='2')):
                    difference = datetime.datetime.now().date() - i.date_joined.date()
                    if difference.days != 0 & difference.days % 3 == 0:
                        try:
                            if i.state == '1':
                                keyboard = telebot_create_inline_btn(i.iduser, Data.objects.get().btn1,
                                                                     Data.objects.get().btn2)
                                if not Data.objects.first().image:
                                    bot.send_message(chat_id=chat.chat_id, text=f'{user_name(i)}\n{text}',
                                                     reply_markup=keyboard,
                                                     parse_mode='HTML')
                                else:
                                    bot.send_photo(chat_id=chat.chat_id, photo=Data.objects.first().image,
                                                   caption=f'{user_name(i)}\n{text}', reply_markup=keyboard,
                                                   parse_mode='HTML')
                            else:
                                chat_url_link_db = chat.url_link
                                for e in Const.LINK:
                                    if chat_url_link_db == e[0]:
                                        chat_url_link = e[1]
                                keyboard_link = telebot_link(chat_url_link)
                                bot.send_message(chat_id=chat.chat_id,
                                                 text=f'{user_name_link(i)}\n'
                                                      f'Вы нажали кнопку <b>Да(согласились с условиями '
                                                      f'{settings.TG_SUPPORT_URL}). Чтобы сделать заказ, '
                                                      f'нажмите кнопку ниже</b>',
                                                 reply_markup=keyboard_link, parse_mode='HTML')
                        except apihelper.ApiException as err:
                            time.sleep(int(str(err).split(' ')[-1]))
                    # elif i.date_joined.date() + datetime.timedelta(days=7) == datetime.datetime.now().date():
                    #     try:
                    #         bot.kick_chat_member(chat.chat_id, i.iduser)
                    #         user = Users.objects.get(iduser=i.iduser)
                    #         user.state = '3'
                    #         user.save()
                    #     except apihelper.ApiException:
                    #         pass
                    else:
                        continue
