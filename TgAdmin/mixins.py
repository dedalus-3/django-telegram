import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import MultipleObjectMixin

from .models import Users, Chat
from .serialization import DateEncoder
from .constants import Const


class ObjectListMixin(MultipleObjectMixin):

    @staticmethod
    def __convert_state():
        date = Users.objects.values('iduser', 'username', 'fullname', 'date_joined', 'chat_id', 'state')
        for i in date:
            try:
                chat_id = i['chat_id']
                chat = Chat.objects.get(id=chat_id)
                i['chat_id'] = chat.name
            except ObjectDoesNotExist:
                i['chat_id'] = ''
            state_key = i['state']
            for e in Const.STATE:
                if state_key == e[0]:
                    i['state'] = e[1]
        return date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_inaction'] = Users.objects.filter(state='1').count()
        context['all_count'] = Users.objects.all().count()
        context['count_click_yes'] = Users.objects.filter(state='2').count()
        context['count_click_no'] = Users.objects.filter(state='3').count()
        context['count_click_yes_tp'] = Users.objects.filter(state='4').count()
        context['count_tp_is_vne'] = Users.objects.filter(state='5').count()
        context['count_is_banned'] = Users.objects.filter(is_banned=True).count()
        context['qs_json'] = json.dumps(list(ObjectListMixin.__convert_state()), cls=DateEncoder)
        return context
