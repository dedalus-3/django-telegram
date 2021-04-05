from django.forms.widgets import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    """
        Переопределение шаблона для изображения
    """
    template_name = 'TgAdmin/clearable_file_input.html'
