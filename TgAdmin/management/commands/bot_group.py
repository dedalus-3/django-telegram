from environs import Env
from aiogram import Bot, Dispatcher, types, executor
from asgiref.sync import sync_to_async

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from TgAdmin.models import Users, Data, Chat
from TgAdmin.constants import Const
from ._keyboards import create_inline_btn, link, link_en

env = Env()
env.read_env()


class Command(BaseCommand):
    help = 'Телеграм бот для чатов'

    def handle(self, *args, **options):
        bot = Bot(token=env.str("BOT_TOKEN"))
        dp = Dispatcher(bot)

        def fullname(first_name: str, last_name: str) -> str:
            full_name = first_name
            if last_name:
                full_name += ' ' + last_name
            return full_name

        def user_name(message) -> str:
            user_id = message['new_chat_member'].get('id')
            if message['new_chat_member'].get('username'):
                return f'Добро пожаловать <a href="tg://user?id={user_id}">' \
                       f'{message["new_chat_member"].get("username")}</a>!'
            elif fullname(message["new_chat_member"].get("first_name"), message["new_chat_member"].get("last_name")):
                first_name = message['new_chat_member'].get('first_name')
                last_name = message['new_chat_member'].get('last_name')
                full_name = fullname(first_name, last_name)
                return f'Добро пожаловать ' \
                       f'<a href="tg://user?id={user_id}">{full_name}</a>!'
            else:
                return f'Добро пожаловать <a href="tg://user?id={user_id}">пользователь</a>!'

        def user_name_en(message) -> str:
            user_id = message['new_chat_member'].get('id')
            if message['new_chat_member'].get('username'):
                return f'Welcome <a href="tg://user?id={user_id}">' \
                       f'{message["new_chat_member"].get("username")}</a>!'
            elif fullname(message["new_chat_member"].get("first_name"), message["new_chat_member"].get("last_name")):
                first_name = message['new_chat_member'].get('first_name')
                last_name = message['new_chat_member'].get('last_name')
                full_name = fullname(first_name, last_name)
                return f'Welcome ' \
                       f'<a href="tg://user?id={user_id}">{full_name}</a>!'
            else:
                return f'Welcome <a href="tg://user?id={user_id}">user</a>!'

        @sync_to_async
        def create_user(id_user, username, full_name, chat_id, state='1'):
            return Users.objects.create(iduser=id_user, username=username, fullname=full_name, state=state,
                                        chat_id=chat_id)

        @sync_to_async
        def select_btn1():
            return Data.objects.get().btn1

        @sync_to_async
        def select_btn1_en():
            return Data.objects.get().btn1_en

        @sync_to_async
        def select_btn2():
            return Data.objects.get().btn2

        @sync_to_async
        def select_btn2_en():
            return Data.objects.get().btn2_en

        @sync_to_async
        def select_text():
            return Data.objects.get().text_before_btn

        @sync_to_async
        def select_text_en():
            return Data.objects.get().text_before_btn_en

        @sync_to_async
        def select_image():
            return Data.objects.get().image

        @sync_to_async
        def state_for_user(user_id, chat_id):
            chat = Chat.objects.get(chat_id=chat_id)
            return Users.objects.get(iduser=user_id, chat_id=chat).state

        @sync_to_async
        def update_state_user(id_user, chat_id, state):
            chat = Chat.objects.get(chat_id=chat_id)
            user = Users.objects.get(iduser=id_user, chat_id=chat)
            user.state = state
            user.save(update_fields=['state'])

        @sync_to_async
        def create_group(chat_id, name, url_chat):
            return Chat.objects.create(chat_id=chat_id, name=name, url_chat=f'https://t.me/{url_chat}')

        @sync_to_async
        def select_group(chat_id):
            try:
                return Chat.objects.get(chat_id=chat_id)
            except ObjectDoesNotExist:
                # TODO на этот счет сделать логирование и потом посмотреть, много ли он косячит
                pass

        @dp.message_handler(commands=['add_group'])
        async def test(message: types.Message):
            user = types.User.get_current()
            if str(user.id) == env.str("ID_ADMIN"):
                try:
                    await create_group(message.chat.id, message.chat.title, message.chat.username)
                    await message.answer(
                        'Группа сохранена в базе данных. Перейдите на сайт администрирования, '
                        'чтобы настроить <b>url техподдержки</b>, <b>язык чата</b> и <b>url чата</b>',
                        parse_mode='HTML')
                except IntegrityError:
                    await message.answer('Данная группа уже добавлена')

        @dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
        async def greeting_member(message: types.Message):
            user_id = message['new_chat_member']['id']
            user_username = message['new_chat_member'].get('username')

            if str(user_id) != env.str("ID_ADMIN"):
                if not message['new_chat_member']['is_bot']:
                    chat = await select_group(message.chat.id)
                    try:
                        first_name = message['new_chat_member'].get('first_name')
                        last_name = message['new_chat_member'].get('last_name')
                        await create_user(id_user=user_id, username=user_username,
                                          full_name=fullname(first_name, last_name),
                                          chat_id=chat)
                    except IntegrityError:
                        pass
                    if chat:
                        if chat.language == 'en':
                            text_btn1 = await select_btn1_en()
                            text_btn2 = await select_btn2_en()
                            if not await select_image():
                                await message.answer(
                                    text=f'{user_name_en(message)}\n{await select_text_en()}',
                                    reply_markup=await create_inline_btn(message["new_chat_member"].get("id"),
                                                                         text_btn1, text_btn2), parse_mode='HTML')
                            else:
                                image = await select_image()
                                await message.answer_photo(
                                    photo=types.InputFile.from_url(f"http://{env.str('IP_DOMAIN')}{image.url}"),
                                    caption=f"{user_name_en(message)}\n{await select_text_en()}",
                                    reply_markup=await create_inline_btn(message["new_chat_member"].get("id"),
                                                                         text_btn1, text_btn2),
                                    parse_mode='HTML')
                        else:
                            text_btn1 = await select_btn1()
                            text_btn2 = await select_btn2()
                            if not await select_image():
                                await message.answer(
                                    text=f'{user_name(message)}\n{await select_text()}',
                                    reply_markup=await create_inline_btn(message["new_chat_member"].get("id"),
                                                                         text_btn1, text_btn2), parse_mode='HTML')
                            else:
                                image = await select_image()
                                await message.answer_photo(
                                    photo=types.InputFile.from_url(f"http://{env.str('IP_DOMAIN')}{image.url}"),
                                    caption=f"{user_name(message)}\n{await select_text()}",
                                    reply_markup=await create_inline_btn(message["new_chat_member"].get("id"),
                                                                         text_btn1, text_btn2),
                                    parse_mode='HTML')
                    else:
                        text_btn1 = await select_btn1()
                        text_btn2 = await select_btn2()
                        if not await select_image():
                            await message.answer(
                                text=f'{user_name(message)}\n{await select_text()}',
                                reply_markup=await create_inline_btn(message["new_chat_member"].get("id"), text_btn1,
                                                                     text_btn2), parse_mode='HTML')
                        else:
                            image = await select_image()
                            await message.answer_photo(
                                photo=types.InputFile.from_url(f"http://{env.str('IP_DOMAIN')}{image.url}"),
                                caption=f"{user_name(message)}\n{await select_text()}",
                                reply_markup=await create_inline_btn(message["new_chat_member"].get("id"), text_btn1,
                                                                     text_btn2),
                                parse_mode='HTML')

        @dp.callback_query_handler(lambda c: c.data == f'yes|{c.from_user.id}')
        async def click_yes(call: types.CallbackQuery):
            chat = await select_group(call.message.chat.id)
            chat_url_link_db = chat.url_link
            for e in Const.LINK:
                if chat_url_link_db == e[0]:
                    chat_url_link = e[1]
            if chat.language == 'en':
                if await state_for_user(call.from_user.id, call.message.chat.id) != '2':
                    await update_state_user(call.from_user.id, call.message.chat.id, '2')
                var_link = await link_en(chat_url_link)
                await call.message.edit_reply_markup(reply_markup=var_link)
            else:
                if await state_for_user(call.from_user.id, call.message.chat.id) != '2':
                    await update_state_user(call.from_user.id, call.message.chat.id, '2')
                var_link = await link(chat_url_link)
                await call.message.edit_reply_markup(reply_markup=var_link)

        @dp.callback_query_handler(lambda c: c.data == f'no|{c.from_user.id}')
        async def click_no(call: types.CallbackQuery):
            await update_state_user(call.from_user.id, call.message.chat.id, '3')
            await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id, until_date=31)

        executor.start_polling(dp, skip_updates=True)
