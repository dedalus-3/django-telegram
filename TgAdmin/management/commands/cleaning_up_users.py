import struct

from django.core.management import BaseCommand

from environs import Env
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PeerIdInvalidError

from TgAdmin.models import Chat, Users

env = Env()
env.read_env()


class Command(BaseCommand):
    help = 'Удаление пользователей'

    def handle(self, *args, **options):
        api_id = env.int('API_ID')
        api_hash = env.str('API_HASH')
        bot_token = env.str('BOT_TOKEN')

        client = TelegramClient('client', api_id, api_hash)

        def get_chats():
            """
            Получаем список всех чатов, исключая созданный руками
            """
            return Chat.objects.values('chat_id').exclude(chat_id='12345')

        async def get_actual_users():
            """
            Получаем список пользователей на текущий момент в чате и удаляем пользователей из БД
            """
            await client.connect()
            info = await client.sign_in()
            for chat in get_chats():
                try:
                    chat_entry = await client.get_entity(int(chat.get('chat_id')))
                except struct.error:
                    continue
                except ValueError:
                    continue
                except PeerIdInvalidError:
                    continue
                else:
                    # Записываем id пользователей в словарь
                    users_id = list()
                    for user in await client.get_participants(chat_entry):
                        users_id.append(str(user.id))
                    # На всякий случай проверку, что список не пуст, чтобы не удалить всех пользователей
                    if users_id:
                        chat_db = Chat.objects.get(chat_id=chat.get('chat_id'))
                        Users.objects.filter(chat_id=chat_db).exclude(iduser__in=users_id).delete()
                        users_id.clear()
                    else:
                        continue

        with client:
            client.loop.run_until_complete(get_actual_users())
