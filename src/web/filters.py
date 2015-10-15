# -*- coding: utf-8; -*-
#
# Licensed to Crate (https://crate.io) under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  Crate licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
# However, if you have executed another commercial license agreement
# with Crate these terms will supersede the license and you may use the
# software solely pursuant to the terms of the relevant commercial agreement.

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
    if not items:
        return []
    return filter(lambda x: needle in x['category'], items)

@register.filter(is_safe=True)
def filter_by_tag(items, needle):
    if not items:
        return []
    return filter(lambda x: needle in x['tags'], items)

@register.filter(is_safe=True)
def filter_by_author(items, author):
    if not items:
        return []
    return filter(lambda x: author == x['author'], items)

