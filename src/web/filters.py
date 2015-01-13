# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import json
import datetime

from django.template.base import Library
from django.utils.safestring import mark_safe

register = Library()


class DateTimeJSONEncoder(json.JSONEncoder):
    """Encoder for datetime objects"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        return super(DateTimeJSONEncoder, self).default(obj)


@register.filter(is_safe=True)
def json_dump(value):
    return json.dumps(value, indent=2, cls=DateTimeJSONEncoder)
