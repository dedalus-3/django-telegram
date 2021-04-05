from solo.admin import SingletonModelAdmin

from django.contrib import admin

from . import models


admin.site.register(models.Users)
admin.site.register(models.Data, SingletonModelAdmin)
admin.site.register(models.TempDataSupport)
admin.site.register(models.TempDataBtn)
admin.site.register(models.Chat)
