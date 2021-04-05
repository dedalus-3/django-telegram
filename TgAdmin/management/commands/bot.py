from environs import Env
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command as Comm
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import exceptions
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from TgAdmin.models import Users, TempDataSupport, TempDataBtn, Chat, Data
from ._keyboards import keyboard_state_1, support_keyboard, after_answer_support, language_inline_btn

env = Env()
env.read_env()


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot = Bot(token=env.str("BOT_TOKEN2"))
        storage = RedisStorage2('127.0.0.1', 6379, db=5, pool_size=10, prefix='wait_for_support_message')
        # storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        id_admin = env.str("ID_ADMIN_FOR_2_BOT")

        async def set_default_commands(dp):
            await dp.bot.set_my_commands([
                types.BotCommand('support', 'Написать сообщение в техподдержку'),
                types.BotCommand('faq', 'Часто задаваемые вопросы'),
            ])

        async def on_shutdown(dp):
            await dp.storage.close()
            await dp.storage.wait_closed()

        @database_sync_to_async
        def get_users(id_user, state=None):
            if state:
                return Users.objects.filter(iduser=id_user, state=state).only('iduser', 'state', 'language')
            return Users.objects.filter(iduser=id_user).only('iduser', 'state', 'language')

        @database_sync_to_async
        def get_user(id_user, state):
            return Users.objects.filter(iduser=id_user, state=state)[0]

        @sync_to_async
        def update_for_user(list_user_id, state_filter, **update_data):
            return Users.objects.filter(iduser__in=list_user_id, state=state_filter).update(**update_data)

        @sync_to_async
        def update_state_user(user, state):
            user.state = state
            user.save(update_fields=['state'])

        @sync_to_async
        def update_banned_user(user, is_banned):
            user.is_banned = is_banned
            user.save(update_fields=['is_banned'])

        @sync_to_async
        def update_language_user(user, language):
            user.language = language
            user.save(update_fields=['language'])

        @sync_to_async
        def create_user(id_user, username, fullname, state: str, chat_id='12345'):
            chat = Chat.objects.get(chat_id=chat_id)
            return Users.objects.create(iduser=id_user, username=username, fullname=fullname, chat_id=chat,
                                        state=state)

        @sync_to_async
        def get_faq():
            return Data.objects.get().faq

        @sync_to_async
        def get_tds(id_user):
            return TempDataSupport.objects.get(id_user=id_user)

        @sync_to_async
        def create_tds(id_message, id_user, text):
            return TempDataSupport.objects.create(id_message=id_message, id_user=id_user, text=text)

        @sync_to_async
        def update_text_tds(obj, text):
            obj.text += f'\n{text}'
            obj.save()

        @sync_to_async
        def delete_obj_tds(id_user):
            return TempDataSupport.objects.get(id_user=id_user).delete()

        @sync_to_async
        def create_obj_tdb(id_message, id_user):
            return TempDataBtn.objects.create(id_message=id_message, id_user=id_user)

        @sync_to_async
        def get_tdb(id_user):
            return TempDataBtn.objects.get(id_user=id_user)

        @sync_to_async
        def delete_obj_tdb(id_user):
            return TempDataBtn.objects.get(id_user=id_user).delete()

        @dp.message_handler(commands=['start'])
        async def welcome_page(message: types.Message):
            users = await get_users(message.from_user.id)
            if not users:
                await create_user(id_user=message.from_user.id, username=message.from_user.username,
                                  fullname=message.from_user.full_name, state='5')
            else:
                if users.filter(state='2'):
                    if users.filter(state='4'):
                        users_id_state_four = []
                        print(users_id_state_four)
                        for user in users.filter('4'):
                            users_id_state_four.append(user.iduser)
                        print(users_id_state_four)
                        await update_for_user(users_id_state_four, '4', is_banned=False)
                        user_state_four = users.filter(state='4')[0]
                        users_id_state_two = []
                        for user in user.filter(state='2'):
                            users_id_state_two.append(user.iduser)
                        await update_for_user(users_id_state_two, '2', state='4', language=user_state_four.language)
                        if user_state_four.language == 'en':
                            await message.answer(text='Enter the command "/support" to ask a question')
                        else:
                            await message.answer(text='Введите команду "/support", чтобы задать вопрос')
                    else:
                        users_id_state_two = []
                        print(users_id_state_two)
                        for user in users.filter(state='2'):
                            users_id_state_two.append(user.iduser)
                        print(users_id_state_two)
                        await update_for_user(users_id_state_two, '2', state='4')
                        await message.answer(text='Выберите язык\n Choose language',
                                             reply_markup=await language_inline_btn())
                elif users.filter(state='4'):
                    users_id_state_four = []
                    for user in users.filter(state='4'):
                        users_id_state_four.append(user.iduser)
                    await update_for_user(users_id_state_four, '4', is_banned=False)
                    user_state_four = await get_user(users_id_state_four[0], '4')
                    if user_state_four.language == 'en':
                        await message.answer(text='Enter the command "/support" to ask a question')
                    else:
                        await message.answer(text='Введите команду "/support", чтобы задать вопрос')
                elif users.filter(state='1'):
                    if len(users.filter(state='1')) == 1:
                        print('Зашел на бездействие, когда длина 1')
                        user = users.filter(state='1')[0]
                        # user = await get_user(message.from_user.id, '1')
                        print(user)
                        try:
                            print('Смог получить url')
                            print(user.chat_id.url_chat)
                            url_chat = user.chat_id.url_chat
                            print(url_chat)
                            print('Получил url')
                            keyboard = await keyboard_state_1(url_chat)
                            await message.answer(text='Вы не ответили в чате, перейдите обратно в чат\n'
                                                      'You have not answered in the chat, go back to the chat',
                                                 reply_markup=keyboard)
                        except AttributeError:
                            print('Не смог получить url')
                            await message.answer(text='Вы не ответили в чате, перейдите обратно в чат\n'
                                                      'You have not answered in the chat, go back to the chat')
                        except exceptions.BadRequest:
                            await message.answer(text='Вы не ответили в чате, перейдите обратно в чат\n'
                                                      'You have not answered in the chat, go back to the chat')
                    else:
                        await message.answer(text='Вы не ответили в чате, перейдите обратно в чат\n'
                                                  'You have not answered in the chat, go back to the chat')
                elif users.filter(state='3'):
                    await message.answer(text='Вам техподдержка не сможет ответить!\n'
                                              'Technical support will not be able to answer you!')

        @dp.callback_query_handler(lambda call: call.data.startswith('language'))
        async def choice_language(call: types.CallbackQuery):
            print(call.data)
            _, language = call.data.split('|')
            print(language)
            print(call.from_user)
            users_id_state_four = []
            if language == 'en':
                users = await get_users(call.from_user.id, '4')
                for user in users:
                    users_id_state_four.append(user.iduser)
                await update_for_user(users_id_state_four, '4', language='en')
                await call.message.answer(text='Enter the command "/support" to ask a question')
            else:
                users = await get_users(call.from_user.id, '4')
                for user in users:
                    users_id_state_four.append(user.iduser)
                await update_for_user(users_id_state_four, '4', language='ru')
                await call.message.answer(text='Введите команду "/support", чтобы задать вопрос')

        @dp.message_handler(Comm('support'))
        async def ask_support(message: types.Message):
            users = await get_users(message.from_user.id)
            if users.filter(state='4'):
                user_state_four = await get_user(message.from_user.id, '4')
                if user_state_four.language == 'en':
                    text = "Want to write a message to tech support? Click on the button below!"
                    keyboard = await support_keyboard(language='en')
                else:
                    text = "Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!"
                    keyboard = await support_keyboard(language='ru')
                await message.answer(text, reply_markup=keyboard)

        @dp.message_handler(Comm('faq'))
        async def faq_support(message: types.Message):
            text = await get_faq()
            await message.answer(text=text)

        @dp.callback_query_handler(lambda call: call.data.startswith('ask_support'))
        async def send_to_support(call: types.CallbackQuery, state: FSMContext):
            _, user_id_str, as_user = call.data.split(':')
            await call.answer()
            user_id = int(user_id_str)
            if user_id_str == id_admin:
                user = await get_user(call.from_user.id, '4')
            else:
                user = await get_user(user_id, '4')
            if as_user == 'no':
                await delete_obj_tds(id_user=user_id)
                await create_obj_tdb(id_message=call.message.message_id, id_user=user_id)
                await call.message.answer('Пришлите Ваше сообщение, которым Вы хотите поделиться')
            else:
                if user.language == 'en':
                    await call.message.answer('Send your message that you want to share')
                else:
                    await call.message.answer('Пришлите Ваше сообщение, которым Вы хотите поделиться')
            await state.set_state('wait_for_support_message')
            await state.update_data(second_id=user_id)
            await state.update_data(as_user=as_user)

        @dp.callback_query_handler(lambda call: call.data.startswith('ask_support'), state='*')
        async def send_to_support(call: types.CallbackQuery):
            await call.answer()

        @dp.message_handler(state='wait_for_support_message', content_types=types.ContentTypes.ANY)
        async def get_support_message(message: types.Message, state: FSMContext):
            data = await state.get_data()
            second_id = data.get('second_id')
            id_user = message.from_user.id
            as_user = data.get('as_user')
            if str(id_user) == id_admin:
                user = await get_user(second_id, '4')
            else:
                user = await get_user(id_user, '4')
            if as_user == 'yes':
                keyboard = await support_keyboard(user_id=message.from_user.id, language='ru')
                try:
                    d = await get_tds(id_user=id_user)
                    await update_text_tds(d, message.text)
                    await bot.edit_message_text(text=f"Вам письмо от @{message.from_user.username}! "
                                                     f"Язык: {user.language}\n\n{d.text}\n"
                                                     f"\nВы можете ответить, нажав кнопку ниже",
                                                chat_id=id_admin, message_id=d.id_message, reply_markup=keyboard)
                except ObjectDoesNotExist:
                    a = await bot.send_message(second_id,
                                               f"Вам письмо от @{message.from_user.username}! Язык: {user.language}"
                                               f"\n\n{message.text}\n"
                                               f"\nВы можете ответить, нажав кнопку ниже", reply_markup=keyboard)
                    await create_tds(id_message=a.message_id, id_user=id_user, text=message.text)
                print(f"id_user: {id_user}, second_id: {second_id}")
                if user.language == 'en':
                    await message.answer("You have sent a question to technical support!")
                else:
                    await message.answer("Вы отправили вопрос в техподдержку!")
            elif as_user == 'no':
                keyboard = await after_answer_support()
                d = await get_tdb(id_user=second_id)
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=d.id_message,
                                                    reply_markup=keyboard)
                await delete_obj_tdb(id_user=second_id)
                if user.language == 'en':
                    await bot.send_message(second_id, f"You received a response from technical support:"
                                                      f"\n\n{message.text}")
                else:
                    await bot.send_message(second_id, f"Вам пришел ответ от техподдержки:\n\n{message.text}")
                await message.answer("Вы ответили пользователю!")
            await state.reset_state()

        @dp.callback_query_handler(lambda call: call.data == 'after_answer')
        async def after_answer(call: types.CallbackQuery):
            await call.answer("Вы уже ответили этому пользователю!", show_alert=True)

        executor.start_polling(dp, on_startup=set_default_commands, on_shutdown=on_shutdown)
