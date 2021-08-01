from aiogram import types


def fullname(first_name: str, last_name: str) -> str:
    full_name = first_name
    if last_name:
        full_name += ' ' + last_name
    return full_name


def user_name(member: types.ChatMemberUpdated) -> str:
    user_id = member.new_chat_member.user.id
    if member.new_chat_member.user.username:
        return f'Добро пожаловать <a href="tg://user?id={user_id}">' \
               f'{member.new_chat_member.user.username}</a>!'
    elif fullname(member.new_chat_member.user.first_name, member.new_chat_member.user.last_name):
        first_name = member.new_chat_member.user.first_name
        last_name = member.new_chat_member.user.last_name
        full_name = fullname(first_name, last_name)
        return f'Добро пожаловать ' \
               f'<a href="tg://user?id={user_id}">{full_name}</a>!'
    else:
        return f'Добро пожаловать <a href="tg://user?id={user_id}">пользователь</a>!'


def user_name_en(member: types.ChatMemberUpdated) -> str:
    user_id = member.new_chat_member.user.id
    if member.new_chat_member.user.username:
        return f'Welcome <a href="tg://user?id={user_id}">' \
               f'{member.new_chat_member.user.username}</a>!'
    elif fullname(member.new_chat_member.user.first_name, member.new_chat_member.user.last_name):
        first_name = member.new_chat_member.user.first_name
        last_name = member.new_chat_member.user.last_name
        full_name = fullname(first_name, last_name)
        return f'Welcome ' \
               f'<a href="tg://user?id={user_id}">{full_name}</a>!'
    else:
        return f'Welcome <a href="tg://user?id={user_id}">user</a>!'
