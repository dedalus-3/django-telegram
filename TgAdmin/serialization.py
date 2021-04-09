import json
import datetime

import pytz
from pytz import timezone


class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # TODO настроить часовую зону, так как при поиске отображается неккоректно
            return obj.strftime("%d/%m/%Y %H:%m")
