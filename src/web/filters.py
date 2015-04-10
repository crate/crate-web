# vim: set fileencodings=utf-8
# -*- coding: utf-8 -*-

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
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return super(DateTimeJSONEncoder, self).default(obj)


@register.filter(is_safe=True)
def json_dump(value):
    return json.dumps(value, indent=2, cls=DateTimeJSONEncoder)

@register.filter(is_safe=True)
def filter_by_category(items, needle):
    return filter(lambda x: needle in x['category'], items)

@register.filter(is_safe=True)
def filter_by_tag(items, needle):
    return filter(lambda x: needle in x['tags'], items)

@register.filter(is_safe=True)
def filter_by_author(items, author):
    return filter(lambda x: author == x['author'], items)

