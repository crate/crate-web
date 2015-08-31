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

CDN_URL = 'https://cdn.crate.io'

def media(context, media_url):
    """
    Get the path for a media file.
    """

    if media_url.startswith('http://') or media_url.startswith('https://'):
        url = media_url
    elif media_url.startswith('/'):
        url = u'{0}{1}'.format(CDN_URL, media_url)
    else:
        url = u'{0}/media/{1}'.format(CDN_URL, media_url)
    return url

register.simple_tag(takes_context=True)(media)

