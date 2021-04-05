from environs import Env

env = Env()
env.read_env()


class Const:
    STATE = [
        ('1', 'Бездействие'),
        ('2', 'Согласен'),
        ('3', 'Не согласен'),
        ('4', 'Согласен+тп'),
        ('5', 'Из-вне'),
    ]

    LANGUAGE = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    LINK = [
        ('tp', env.str("TG_SUPPORT_URL")),
        ('sh', env.str("TG_SHOP_URL")),
    ]

    LANGUAGE_SUPPORT = [
        ('no', None),
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    TEXT_FOR_FAQ = """
    Здесь будут ответы на часто задаваевые вопросы!
    Сейчас введите команду "/support", чтобы задать вопрос в техподдержку.
    """