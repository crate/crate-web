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

from datetime import datetime
from markdown2 import markdown

from django.template import Context
from django.template.base import Library
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from web.utils import toDict, parseDate, parsePost

DIR = 'blog/'
POSTS = []
NEWS_JSON = []
DEVELOPER_NEWS_JSON = []

# https://github.com/trentm/python-markdown2/wiki/link-patterns
link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]

def filterPosts(posts, categ):
    return filter(lambda x: categ in x.get('category'), posts)


def preBuild(site):

    global POSTS
    global NEWS_JSON
    global DEVELOPER_NEWS_JSON

    # Build all the posts
    for page in site.pages():
        if page.path.startswith(DIR):

            # Skip non html posts for obvious reasons
            if not page.path.endswith('.html'):
                continue

            # Parse headers and markdown body
            headers, body = parsePost(page)

            # Build a context for each post
            postContext = Context()
            postContext.update(headers)
            postContext['raw_body'] = body
            postContext['path'] = page.path
            postContext['date'] = parseDate(headers.get('date') or headers.get('created'))
            postContext['url'] = page.absolute_final_url
            postContext['tags'] = headers.get('tags') and [h.strip() for h in headers['tags'].split(',')] or []
            postContext['category'] = headers.get('category') and [h.strip() for h in headers['category'].split(',')] or []
            POSTS.append(postContext)

    # Sort the posts by date
    POSTS = sorted(POSTS, key=lambda x: x['date'])
    POSTS.reverse()

    indexes = range(0, len(POSTS))

    for i in indexes:
        if i+1 in indexes: POSTS[i]['prev_post'] = POSTS[i+1]
        if i-1 in indexes: POSTS[i]['next_post'] = POSTS[i-1]

    settings = site.config.get('settings', {})
    NEWS_JSON = toDict(settings, filterPosts(POSTS, 'news'))
    DEVELOPER_NEWS_JSON = toDict(settings, filterPosts(POSTS, 'developernews'))


def preBuildPage(site, page, context, data):
    """
    Add the list of posts to every page context so we can
    access them from wherever on the site.
    """
    context['posts'] = POSTS
    context['news_json'] = NEWS_JSON
    context['developer_news_json'] = DEVELOPER_NEWS_JSON

    for post in POSTS:
        if post['path'] == page.path:
            tpl = get_template(post.get('template', 'post.html'))
            raw = force_text(post['raw_body'])
            post['body'] = mark_safe(markdown(raw,
                extras=["fenced-code-blocks","header-ids"]))
            context['__CACTUS_CURRENT_PAGE__'] = page
            context['CURRENT_PAGE'] = page
            context.update(post)
            data = tpl.render(context)

    return context, data

