import asyncio

from environs import Env
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.exceptions import RetryAfter

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db import transaction

from TgAdmin.constants import Const
from ._keyboards import create_inline_btn, link, link_en
from . import _db as db
from . import _common as common

env = Env()
env.read_env()


class Command(BaseCommand):
    help = 'Телеграм бот для чатов'

    def handle(self, *args, **options):
        bot = Bot(token=env.str("BOT_TOKEN"))
        dp = Dispatcher(bot)

        async def bot_send_message_user(chat_member, btn1, btn2):
            """
            Отправляет сообщение в чат
            """
            return await bot.send_message(
                chat_id=chat_member.chat.id,
                text=f'{common.user_name_en(chat_member)}\n{await db.select_text_en()}',
                parse_mode='HTML',
                reply_markup=await create_inline_btn(
                    chat_member.new_chat_member.user.id,
                    btn1,
                    btn2,
                ),
            )

        async def bot_send_photo_user(chat_member, btn1, btn2, image):
            """
            Отправляет фотографию в чат
            """
            return await bot.send_photo(
                chat_id=chat_member.chat.id,
                photo=types.InputFile.from_url(f"http://{env.str('IP_DOMAIN')}{image.url}"),
                caption=f"{common.user_name_en(chat_member)}\n{await db.select_text_en()}",
                parse_mode='HTML',
                reply_markup=await create_inline_btn(
                    chat_member.new_chat_member.user.id,
                    btn1,
                    btn2,
                ),
            )

        async def bot_send_photo_or_message_user(func, user_id, chat_id, **kwargs):
            """
            Обработчка исключения RetryAfter telegram
            """
            try:
                msg = await func(**kwargs)
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
                msg = await func(**kwargs)
            await db.update_message_id(
                user_id=user_id,
                chat_id=chat_id,
                message_id=msg.message_id
            )

        async def check_image(user_id, chat_id, chat_member, btn1, btn2, image):
            """
            Проверка изображения в админке
            """
            if not image:
                await bot_send_photo_or_message_user(
                    bot_send_message_user,
                    user_id,
                    chat_id,
                    chat_member=chat_member,
                    btn1=btn1,
                    btn2=btn2,
                )
            else:
                await bot_send_photo_or_message_user(
                    bot_send_photo_user,
                    user_id,
                    chat_id,
                    chat_member=chat_member,
                    btn1=btn1,
                    btn2=btn2,
                    image=image,
                )

        @dp.message_handler(commands=['add_group'])
        async def test(message: types.Message):
            """
            Добавление чата в БД
            """
            user = types.User.get_current()
            if str(user.id) == env.str("ID_ADMIN"):
                try:
                    await db.create_group(message.chat.id, message.chat.title, message.chat.username)
                    await message.answer(
                        'Группа сохранена в базе данных. Перейдите на сайт администрирования, '
                        'чтобы настроить <b>url техподдержки</b>, <b>язык чата</b> и <b>url чата</b>',
                        parse_mode='HTML')
                except IntegrityError:
                    await message.answer('Данная группа уже добавлена')
            else:
                await message.answer('Вы не являетесь владельцем чата!')

        @dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
        async def left_member(message: types.Message):
            """
            Удаление пользователя из БД, когда покидает чат
            """
            await db.delete_user(message.left_chat_member.id, message.chat.id)

        @dp.chat_member_handler()
        async def text_message(chat_member: types.ChatMemberUpdated):
            """
            Добавление пользователя в БД, когда вступает в чат
            """
            new_status = chat_member.new_chat_member.status
            old_status = chat_member.old_chat_member.status
            if old_status == 'left' and new_status == 'member':
                user_id = chat_member.new_chat_member.user.id
                user_username = chat_member.new_chat_member.user.username

                if user_id != env.str('ID_ADMIN') and not chat_member.new_chat_member.user.is_bot:
                    chat = await db.select_group(str(chat_member.chat.id))
                    try:
                        full_name = common.fullname(
                            chat_member.new_chat_member.user.first_name,
                            chat_member.new_chat_member.user.last_name,
                        )
                        await db.create_user(
                            id_user=user_id,
                            username=user_username,
                            chat_id=chat,
                            full_name=full_name,
                        )
                    except IntegrityError:
                        pass

                    if chat:
                        # Английский чат
                        if chat.language == 'en':
                            await check_image(
                                chat_member=chat_member,
                                user_id=user_id,
                                chat_id=chat.chat_id,
                                btn1=await db.select_btn1_en(),
                                btn2=await db.select_btn2_en(),
                                image=await db.select_image()
                            )
                        else:
                            await check_image(
                                chat_member=chat_member,
                                user_id=user_id,
                                chat_id=chat.chat_id,
                                btn1=await db.select_btn1(),
                                btn2=await db.select_btn2(),
                                image=await db.select_image()
                            )
                    # Чат не выбран
                    else:
                        await check_image(
                            chat_member=chat_member,
                            user_id=user_id,
                            chat_id=chat.chat_id,
                            btn1=await db.select_btn1(),
                            btn2=await db.select_btn2(),
                            image=await db.select_image()
                        )

        @dp.callback_query_handler(lambda c: c.data == f'yes|{c.from_user.id}')
        async def click_yes(call: types.CallbackQuery):
            """
            Действие на кнопку, когда пользователь согласен
            """
            chat = await db.select_group(call.message.chat.id)
            if chat:
                chat_url_link_db = chat.url_link
                chat_url_link = None
                for e in Const.LINK:
                    if chat_url_link_db == e[0]:
                        chat_url_link = e[1]
                if chat.language == 'en':
                    if await db.state_for_user(call.from_user.id, call.message.chat.id) == '1':
                        await db.update_state_user(call.from_user.id, call.message.chat.id, '2')
                    var_link = await link_en(chat_url_link)
                    await call.message.edit_reply_markup(reply_markup=var_link)
                else:
                    if await db.state_for_user(call.from_user.id, call.message.chat.id) == '1':
                        await db.update_state_user(call.from_user.id, call.message.chat.id, '2')
                    var_link = await link(chat_url_link)
                    await call.message.edit_reply_markup(reply_markup=var_link)
            else:
                users = await db.state_for_user_no_group(call.from_user.id)
                users_list = []
                for user in users:
                    if user.state not in ['2', '3', '4']:
                        users_list.append(user.iduser)
                await db.update_state_user_no_group(users_list, '2')
                var_link = await link(Const.LINK[0][1])
                await call.message.edit_reply_markup(reply_markup=var_link)

        @dp.callback_query_handler(lambda c: c.data == f'no|{c.from_user.id}')
        @transaction.atomic
        async def click_no(call: types.CallbackQuery):
            """
            Действие пользователя, когда пользователь не согласен
            """
            await db.delete_user(call.from_user.id, call.message.chat.id)
            await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id, until_date=31)

        executor.start_polling(dp, skip_updates=True, allowed_updates=types.AllowedUpdates.all())
