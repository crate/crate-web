# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import os
import re
import json

from datetime import datetime
from markdown2 import markdown

from django.template import Context
from django.template.base import Library
from django.template.loader import get_template, add_to_builtins
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from web.utils import toDict, parseDate, parsePost

DIR = 'blog/'
POSTS = []
NEWS_JSON = []
DEVELOPER_NEWS_JSON = []
CONFIG = {}

add_to_builtins('web.filters')
add_to_builtins('web.tags')


def filterPosts(posts, categ):
    return filter(lambda x: categ in x.get('category'), posts)


def preBuild(site):

    global POSTS
    global NEWS_JSON
    global DEVELOPER_NEWS_JSON

    global CONFIG

    conf = os.path.join(site.path, 'config.json')
    CONFIG = json.load(open(conf,'r'))

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

    indexes = xrange(0, len(POSTS))

    for i in indexes:
        if i+1 in indexes: POSTS[i]['prev_post'] = POSTS[i+1]
        if i-1 in indexes: POSTS[i]['next_post'] = POSTS[i-1]

    NEWS_JSON = toDict(CONFIG, filterPosts(POSTS, 'news'))
    DEVELOPER_NEWS_JSON = toDict(CONFIG, filterPosts(POSTS, 'developernews'))


def preBuildPage(site, page, context, data):
    """
    Add the list of posts to every page context so we can
    access them from wherever on the site.
    """
    context['posts'] = POSTS
    context['news_json'] = NEWS_JSON
    context['developer_news_json'] = DEVELOPER_NEWS_JSON
    context['CONFIG'] = CONFIG

    for post in POSTS:
        if post['path'] == page.path:
            tpl = get_template(post.get('template', 'post.html'))
            raw = force_unicode(post['raw_body'])
            post['body'] = mark_safe(markdown(raw, extras=["fenced-code-blocks"]))
            context['__CACTUS_CURRENT_PAGE__'] = page
            context.update(post)
            data = tpl.render(context)

    return context, data

