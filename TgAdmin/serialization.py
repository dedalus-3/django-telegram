import json
import datetime


class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # TODO настроить часовую зону, так как при поиске отображается неккоректно
            # Сейчас в settings выставил timezone UTC и все нормально, но это не решение
            return obj.strftime("%d/%m/%Y %H:%m")
