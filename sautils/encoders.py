from datetime import datetime
from datetime import timedelta
import json


class DateTimeEncoder(json.JSONEncoder):
    """JSONEncoder that encodes datetime and timedelta instances as strings."""

    def default(self, obj):
        if isinstance(obj, (datetime, timedelta)):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

