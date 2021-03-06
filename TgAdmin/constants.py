from django.conf import settings


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
        ('tp', settings.TG_SUPPORT_URL),
        # ('sh', settings.TG_SHOP_URL),
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

    TEXT_FOR_FAQ_EN = """
    Here are the answers to frequently asked questions!
    Now enter the command "/support" to ask a question to technical support.
    """