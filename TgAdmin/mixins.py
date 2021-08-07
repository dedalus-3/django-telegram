from django.views.generic.list import MultipleObjectMixin

from TgAdmin.models import Users


class ObjectListMixin(MultipleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_inaction'] = Users.objects.filter(state='1').count()
        context['all_count'] = Users.objects.all().count()
        context['count_click_yes'] = Users.objects.filter(state='2').count()
        context['count_click_no'] = Users.objects.filter(state='3').count()
        context['count_click_yes_tp'] = Users.objects.filter(state='4').count()
        context['count_tp_is_vne'] = Users.objects.filter(state='5').count()
        context['count_is_banned'] = Users.objects.filter(is_banned=True).count()
        return context
