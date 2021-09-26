from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from TgAdmin import models


@sync_to_async
def create_user(id_user, username, full_name, chat_id, state='1'):
    return models.Users.objects.create(
        iduser=id_user,
        username=username,
        fullname=full_name,
        state=state,
        chat_id=chat_id
    )


@sync_to_async
def select_btn1():
    return models.Data.objects.get().btn1


@sync_to_async
def select_btn1_en():
    return models.Data.objects.get().btn1_en


@sync_to_async
def select_btn2():
    return models.Data.objects.get().btn2


@sync_to_async
def select_btn2_en():
    return models.Data.objects.get().btn2_en


@sync_to_async
def select_text():
    return models.Data.objects.get().text_before_btn


@sync_to_async
def select_text_en():
    return models.Data.objects.get().text_before_btn_en


@sync_to_async
def select_image():
    return models.Data.objects.get().image


@sync_to_async
def state_for_user(user_id, chat_id):
    chat = models.Chat.objects.get(chat_id=chat_id)
    return models.Users.objects.get(iduser=user_id, chat_id=chat).state


@sync_to_async
def update_state_user(id_user, chat_id, state):
    chat = models.Chat.objects.get(chat_id=chat_id)
    user = models.Users.objects.get(iduser=id_user, chat_id=chat)
    user.state = state
    user.save(update_fields=['state'])


@sync_to_async
def state_for_user_no_group(id_user):
    return models.Users.objects.filter(iduser=id_user)


@sync_to_async
def update_state_user_no_group(id_user, state):
    return models.Users.objects.filter(iduser__in=id_user).update(state=state)


@sync_to_async
def create_group(chat_id, name, url_chat):
    return models.Chat.objects.create(
        chat_id=chat_id,
        name=name,
        url_chat=f'https://t.me/{url_chat}',
    )


@sync_to_async
def select_group(chat_id):
    try:
        return models.Chat.objects.get(chat_id=chat_id)
    except models.Chat.DoesNotExist:
        return None


@sync_to_async
def update_message_id(user_id, chat_id, message_id):
    chat = models.Chat.objects.get(chat_id=chat_id)
    user = models.Users.objects.get(iduser=user_id, chat_id=chat)
    user.message_id = message_id
    user.save(update_fields=['message_id'])


@sync_to_async
def delete_user(user_id, chat_id):
    try:
        chat = models.Chat.objects.get(chat_id=chat_id)
        return models.Users.objects.get(iduser=user_id, chat_id=chat).delete()
    except ObjectDoesNotExist:
        pass


@sync_to_async
def get_id_admin():
    return models.Data.objects.get().id_admin
