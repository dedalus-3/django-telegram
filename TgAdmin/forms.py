from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea

from .widgets import MyClearableFileInput
from .models import Data, Chat


class TextForm(ModelForm):
    class Meta:
        model = Data
        fields = ['text_before_btn', 'text_before_btn_en', 'image']
        widgets = {
            'image': MyClearableFileInput(),  # TODO сделать в шаблоне ссылку на изображение
        }


class BtnYes(ModelForm):
    class Meta:
        model = Data
        fields = ('btn1', 'btn1_en')
        widgets = {
            'btn1': TextInput(attrs={'class': 'form-control'}),
            'btn1_en': TextInput(attrs={'class': 'form-control'}),
        }


class BtnNo(ModelForm):
    class Meta:
        model = Data
        fields = ('btn2', 'btn2_en')
        widgets = {
            'btn2': TextInput(attrs={'class': 'form-control'}),
            'btn2_en': TextInput(attrs={'class': 'form-control'}),
        }


class FaqForm(ModelForm):
    class Meta:
        model = Data
        fields = ('faq', 'faq_en')
        widgets = {
            'faq': Textarea(attrs={'class': 'form-control'}),
            'faq_en': Textarea(attrs={'class': 'form-control'}),
        }


class MailingForm(ModelForm):
    id_user = forms.CharField(label='Id пользователя',
                              help_text='Укажите id пользователя, если хотите отправить сообщение '
                                        'конкретному пользователю',
                              required=False,
                              widget=TextInput(attrs={'class': 'form-control', 'placeholder': '123456789'}))
    image_mailing = forms.ImageField(label='Изображение', required=False)

    class Meta:
        model = Data
        fields = ('text_mailing',)
        widgets = {
            'text_mailing': Textarea(attrs={'class': 'form-control'}),
        }


class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'
        widgets = {
            'chat_id': TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'name': TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'url_link': Select(attrs={'class': 'form-control'}),
            'language': Select(attrs={'class': 'form-control'}),
            'url_chat': TextInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/test_bot'}),
        }
