from django.template import RequestContext
from environs import Env
from telebot import TeleBot
from telebot import apihelper

from django.conf import settings
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Users, Data, Chat
from .forms import TextForm, BtnYes, BtnNo, MailingForm, ChatForm, FaqForm
from .mixins import ObjectListMixin


env = Env()
env.read_env()


class ChatView(LoginRequiredMixin, ListView):
    """
        Список чатов
    """
    template_name = "TgAdmin/chats.html"
    model = Chat


class ChatUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Изменение параметров чата
    """
    model = Chat
    template_name = 'TgAdmin/edit_chat.html'
    form_class = ChatForm
    success_message = 'Данные успешно изменены'


class ChatDeleteView(DeleteView):
    """
        Удаление чата
    """
    model = Chat
    template_name = 'TgAdmin/delete_chat.html'
    success_url = reverse_lazy('chats')


class HomeView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список всех пользователей
    """
    template_name = "TgAdmin/home.html"
    model = Users
    paginate_by = 10


class InactionView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список пользователей, которые бездействуют
    """
    template_name = "TgAdmin/inaction_users.html"
    model = Users
    paginate_by = 10

    def get_queryset(self):
        return Users.objects.filter(state='1')


class ClickYesView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список пользователей, которые нажали "да" в чате
    """
    template_name = "TgAdmin/click_yes_users.html"
    model = Users
    paginate_by = 10

    def get_queryset(self):
        return Users.objects.filter(state='2')


class ClickNoView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список пользователей, которые нажали "нет" в чате
    """
    template_name = 'TgAdmin/click_no_users.html'
    model = Users
    paginate_by = 10

    def get_queryset(self):
        return Users.objects.filter(state='3')


class ClickYesTpView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список пользователей, которые нажали "да" в чате и отписали в техподдержку
    """
    template_name = 'TgAdmin/click_yes_tp_users.html'
    model = Users
    paginate_by = 10

    def get_queryset(self):
        return Users.objects.filter(state='4')


class IsVneView(LoginRequiredMixin, ObjectListMixin, ListView):
    """
        Список пользователей, которые написали в техподдержку из-вне группы
    """
    template_name = 'TgAdmin/isvne_users.html'
    model = Users
    paginate_by = 10

    def get_queryset(self):
        return Users.objects.filter(state='5')


class UpdateText(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Обновление текста в групповом чате при вступлении пользователя
    """
    model = Data
    template_name = 'TgAdmin/text_create.html'
    form_class = TextForm
    success_message = 'Текст/изображение для приветствия новых пользователей успешно изменен'

    def get_object(self, queryset=None):
        return Data.get_solo()

    def get_success_url(self):
        return reverse('text_create')


class UpdateBtnYes(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Обновление кнопки согласия
    """
    model = Data
    template_name = 'TgAdmin/btn1_create.html'
    form_class = BtnYes
    success_message = 'Клавиатура "согласен" успешно изменена'

    def get_object(self, queryset=None):
        return Data.get_solo()

    def get_success_url(self):
        return reverse('btn1_create')


class UpdateBtnNo(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Обновление кнопки отклонения
    """
    model = Data
    template_name = 'TgAdmin/btn2_create.html'
    form_class = BtnNo
    success_message = 'Клавиатура "отклонить" успешно изменена'

    def get_object(self, queryset=None):
        return Data.get_solo()

    def get_success_url(self):
        return reverse('btn2_create')


class UpdateFaq(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Обновление FAQ для техподдержки
    """
    model = Data
    template_name = 'TgAdmin/edit_faq.html'
    form_class = FaqForm
    success_message = 'Текст для FAQ успешно изменен'

    def get_object(self, queryset=None):
        return Data.get_solo()

    def get_success_url(self):
        return reverse('edit_faq')


class LoginUserView(LoginView):
    template_name = 'TgAdmin/login.html'


class LogoutThenLoginView(LoginRequiredMixin, LogoutView):
    login_url = None

    @property
    def next_page(self):
        return self.login_url or settings.LOGIN_URL


class UpdateMailingView(LoginRequiredMixin, UpdateView):
    """
        Рассылка сообщений пользователям в техподдержке
    """
    model = Data
    template_name = 'TgAdmin/mailing_create.html'
    form_class = MailingForm

    def get_object(self, queryset=None):
        return Data.objects.first()

    def get_success_url(self) -> str:
        return reverse('mailing')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        bot = TeleBot(token=env.str("BOT_TOKEN2"))
        if request.POST['id_user']:
            if Users.objects.filter(iduser=request.POST['id_user']):
                try:
                    if request.FILES.get('image_mailing'):
                        bot.send_photo(chat_id=request.POST['id_user'], photo=request.FILES.get('image_mailing'),
                                       caption=request.POST['text_mailing'], parse_mode='HTML')
                    else:
                        bot.send_message(chat_id=request.POST['id_user'], text=request.POST['text_mailing'],
                                         parse_mode='HTML')
                    messages.success(self.request, 'Сообщение отправлено пользователю!')
                except apihelper.ApiException:
                    messages.error(self.request, 'Пользователь остановил бота')
            else:
                messages.error(self.request, 'Данного пользователя нет в вашей базе')
        else:
            users = Users.objects.filter(Q(state='4') & Q(is_banned=False)).order_by('iduser').distinct('iduser')
            try:
                if request.FILES.get('image_mailing'):
                    for user in users:
                        bot.send_photo(chat_id=user.iduser, photo=request.FILES.get('image_mailing'),
                                       caption=request.POST['text_mailing'], parse_mode='HTML')
                else:
                    for user in users:
                        bot.send_message(chat_id=user.iduser, text=request.POST['text_mailing'], parse_mode='HTML')
                messages.success(self.request, 'Рассылка пользователям успешно выполнена')
            except apihelper.ApiException:
                users = Users.objects.filter(iduser=user.iduser, state='4')
                for usr in users:
                    usr.is_banned = True
                    usr.save(update_fields=['is_banned'])
                messages.success(self.request, 'Рассылка пользователям успешно выполнена')
        return super().post(request, *args, **kwargs)
