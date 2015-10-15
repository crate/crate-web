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


import os
import re
import json
import logging

from datetime import datetime
from markdown2 import markdown

from django.template import Context
from django.template.base import Library
from django.template.loader import get_template, add_to_builtins
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from web.utils import toDict, parseDate, parsePost

logger = logging.getLogger(__name__)

DIR = 'events/'
EVENTS = []
PAST_EVENTS = []
UPCOMING_EVENTS = []

def preBuild(site):
    global EVENTS
    global UPCOMING_EVENTS
    global PAST_EVENTS
    for event in site.pages():
        if event.path.startswith(DIR):

            # Skip non html posts for obvious reasons
            if not event.path.endswith('.html'):
                continue

            # Parse headers and markdown body
            headers, body = parsePost(event)
            ctx = Context()
            ctx.update(headers)
            ctx['raw_body'] = body
            ctx['path'] = event.path
            ctx['url'] = event.absolute_final_url
            ctx['date_from'] = parseDate(headers.get('date_from'))
            ctx['date_to'] = parseDate(headers.get('date_to'))
            ctx['tags'] = headers.get('tags') and [h.strip() for h in headers['tags'].split(',')] or []
            EVENTS.append(ctx)

    # Sort the posts by date
    today = datetime.today()
    EVENTS = sorted(EVENTS, key=lambda x: x['date_from'])
    EVENTS.reverse()
    PAST_EVENTS = list(filter(lambda x: x['date_to'] < today, EVENTS))
    UPCOMING_EVENTS = list(filter(lambda x: x['date_to'] >= today, EVENTS))
    UPCOMING_EVENTS.reverse()


def preBuildPage(site, page, context, data):
    """
    Add the list of posts to every page context so we can
    access them from wherever on the site.
    """
    context['events'] = EVENTS
    context['upcoming_events'] = UPCOMING_EVENTS
    context['past_events'] = PAST_EVENTS

    for ctx in EVENTS:
        if ctx['path'] == page.path:
            tpl = get_template(ctx.get('template', 'event.html'))
            raw = force_text(ctx['raw_body'])
            ctx['body'] = mark_safe(markdown(raw, extras=["fenced-code-blocks"]))
            context['__CACTUS_CURRENT_PAGE__'] = page
            context['CURRENT_PAGE'] = page
            context.update(ctx)
            data = tpl.render(context)

    return context, data

