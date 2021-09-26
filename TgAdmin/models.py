from mdeditor.fields import MDTextField
from solo.models import SingletonModel

from django.db import models
from django.urls import reverse

from TgAdmin.constants import Const


class Chat(models.Model):
    class Meta:
        verbose_name = 'Название чата'
        verbose_name_plural = 'Названия чатов'

    chat_id = models.CharField(
        max_length=255,
        verbose_name='Id группы',
        unique=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название группы'
    )
    url_link = models.CharField(
        max_length=255,
        verbose_name='Ссылка на тп/магазин',
        choices=Const.LINK,
        default='tp',
        help_text='Выбрать ссылку для перехода пользователя, после нажатия'
                  ' на клавишу "согласен"'
    )
    # здесь language нужен для группового чата
    language = models.CharField(
        max_length=2,
        choices=Const.LANGUAGE,
        default='ru',
        verbose_name='Язык'
    )
    url_chat = models.URLField(
        max_length=255,
        verbose_name='Ссылка на чат',
        blank=True,
        null=True,
        help_text='По умолчанию добавляется ссылка чата. Если измените ссылку-приглашение, то'
                  ' здесь необходимо изменить ссылку'
    )

    def __str__(self):
        return f"chat_id: {self.chat_id}; name: {self.name}"

    def get_absolute_url(self):
        return reverse('chat_edit', args=[str(self.id)])


class Users(models.Model):
    class Meta:
        verbose_name = 'Пользователь телеграма'
        verbose_name_plural = 'Пользователи телеграма'
        ordering = ['-date_joined']
        unique_together = [['iduser', 'chat_id']]

    iduser = models.CharField(
        max_length=255,
        verbose_name='ID пользователя',
        db_index=True
    )
    username = models.CharField(
        max_length=255,
        verbose_name='Username пользователя',
        blank=True,
        null=True,
    )
    fullname = models.CharField(
        max_length=255,
        verbose_name='Полное имя пользователя',
        blank=True,
        null=True
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления пользователя'
    )
    state = models.CharField(
        max_length=1,
        choices=Const.STATE,
        default='1',
        db_index=True
    )
    chat_id = models.ForeignKey(
        Chat,
        on_delete=models.SET_NULL,
        null=True,
        related_name='users'
    )
    is_banned = models.BooleanField(default=False)
    # Здесь language нужен для техподдержки
    language = models.CharField(
        max_length=2,
        choices=Const.LANGUAGE_SUPPORT,
        default='no'
    )
    message_id = models.CharField(
        max_length=255,
        verbose_name="Id сообщения при вступлении в группу",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"id-{self.iduser}: username-{self.username}, fullname-{self.fullname}"


def user_directory_path(instance, filename):
    return '{0}'.format(filename)


class Data(SingletonModel):
    class Meta:
        verbose_name = 'Данные для изменения'

    text_before_btn = MDTextField(
        verbose_name='Текст рядом с кнопками (русский)',
        default='Текст для приветствия новых пользователей в чате на русском языке'
    )
    text_before_btn_en = MDTextField(
        verbose_name='Текст рядом с кнопками (english)',
        default='Текст для приветствия новых пользователей в чате на английском языке'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=user_directory_path,
        verbose_name='Фотография для текста'
    )
    btn1 = models.CharField(
        max_length=255,
        verbose_name='Кнопка 1 (русский)',
        default='Согласен'
    )
    btn1_en = models.CharField(
        max_length=255,
        verbose_name='Кнопка 1 (english)',
        default='Agree'
    )
    btn2 = models.CharField(
        max_length=255,
        verbose_name='Кнопка 2 (русский)',
        default='Отклонить'
    )
    btn2_en = models.CharField(
        max_length=255,
        verbose_name='Кнопка 2 (english)',
        default='Reject'
    )
    faq = models.TextField(
        verbose_name='FAQ для техподдержки',
        default=Const.TEXT_FOR_FAQ
    )
    faq_en = models.TextField(
        verbose_name='FAQ english для техподдержки',
        default=Const.TEXT_FOR_FAQ_EN
    )
    text_mailing = models.TextField(
        verbose_name='Текс для рассылки в техподдержке',
        default='Текст для рассылки'
    )
    id_admin = models.CharField(
        max_length=100,
        verbose_name='ID пользователя',
        help_text='ID пользователя, кто будет добавлять чаты в БД',
        default='',
    )

    def __str__(self):
        return 'Данные для изменения'


class TempDataSupport(models.Model):
    class Meta:
        verbose_name = 'Временные данные техподдержки'
        verbose_name_plural = 'Временные данные техподдержки'

    id_message = models.CharField(
        max_length=255,
        verbose_name='ID сообщения в техподдержке'
    )
    id_user = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ID пользователя'
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
        blank=True,
        null=True
    )

    def __str__(self):
        return 'Временные данные техподдержки'


class TempDataBtn(models.Model):
    class Meta:
        verbose_name = 'Временные данные для обработчика'
        verbose_name_plural = 'Временные данные для обработчика'

    id_message = models.CharField(
        max_length=255,
        verbose_name="ID сообщения в техподдержке"
    )
    id_user = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ID пользователя'
    )

    def __str__(self):
        return 'Временные данные для обработчика'
