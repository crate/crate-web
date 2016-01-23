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
import time

from datetime import datetime
from markdown2 import markdown

from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from web.utils import toDict, parseDate, parsePost

COLLECTIONS = dict()
COLLECTIONS_JSON = dict()
# legacy stuff
NEWS_JSON = []
DEVELOPER_NEWS_JSON = []

# For a full list of available extras see
# https://github.com/trentm/python-markdown2/wiki/Extras
MARKDOWN_EXTRAS = [
    "fenced-code-blocks",
    "code-friendly",
    "header-ids",
    "tables",
]

class Collection(object):

    CONTEXT_RAW_KEY = 'raw_body'
    CONTEXT_OUTPUT_KEY = 'body'

    def __init__(self, title, path, template, root_path, pages=[], config={}):
        self.title = title
        self.path = path
        self.template = template
        self.config = config
        self.root_path = root_path
        self.pages = self.create_contexts(self._apply_filter(pages))
        self._build_page_index()

    def _apply_filter(self, pages):
        return [p for p in pages \
                if p.path.startswith(self.path) \
                and p.path.endswith('.html')]

    def contains_page(self, page):
        """Check if page is part of the collection."""
        return page.path in self.__paths

    def page_context(self, page):
        """Throws ValueError if page is not part of the collection"""
        idx = self.__paths.index(page.path)
        return self.pages[idx]

    def create_contexts(self, pages):
        contexts = []
        for page in pages:
            # Parse headers and markdown body
            headers, body = parsePost(page.data())
            # Build a context for each post
            ctx = Context()
            ctx.update(headers)
            ctx[Collection.CONTEXT_RAW_KEY] = body
            ctx['path'] = page.path
            ctx['date'] = Collection.to_datetime(headers)
            ctx['url'] = page.absolute_final_url
            for list_type in ['tags', 'category', 'topics']:
                ctx[list_type] = Collection.to_list(headers, list_type)
            contexts.append(ctx)
        return contexts

    def _build_page_index(self):
        self.__paths = []
        for ctx in self.pages:
            self.__paths.append(ctx['path'])

    @staticmethod
    def to_list(headers, key):
        if headers.get(key):
            return [h.strip() for h in headers[key].split(',')]
        return []

    @staticmethod
    def to_datetime(headers):
        return parseDate(headers.get('date') or headers.get('created'))

    def filter(self, value, key='tags'):
        return filter(lambda p: value in p.get(key), self.pages)

    def sort(self, key=None, toc=None, reverse=False):
        if not key and toc:
            self.pages = self._sort_by_toc(toc)
            self.pages.reverse()
        elif key and not toc:
            self.pages = sorted(self.pages, key=lambda x: x[key])
            if reverse:
                self.pages.reverse()
        self._build_page_index()

    def _sort_by_toc(self, toc_file):
        """Orders the page contexts as defined in a toc file."""
        if os.path.isabs(toc_file):
            filepath = toc_file
        else:
            filepath = os.path.abspath(os.path.join(self.root_path, 'pages', toc_file))

        print (filepath)
        lines = []
        with open(filepath) as fp:
            [lines.append(line.rstrip()) for line in fp]

        sorted_pages = [None for x in range(len(lines))]
        for page in self.pages:
            try:
                idx = lines.index(page['path'])
            except ValueError as e:
                # ignore files that are not in collection
                pass
            else:
                sorted_pages[idx] = page
        # return cleaned up list
        return [x for x in sorted_pages if x is not None]

    def create_navigation(self):
        indexes = range(0, len(self.pages))
        for i in indexes:
            if i+1 in indexes: self.pages[i]['prev_post'] = self.pages[i+1]
            if i-1 in indexes: self.pages[i]['next_post'] = self.pages[i-1]

    def serialize(self):
        return toDict(self.config.get('settings', {}), self.pages)

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def __iter__(self):
        return self.pages.__iter__()

    def __repr__(self):
        return '<{0}: {1} ({2} pages)>'.format(self.title, self.path, len(self.pages))


def preBuild(site):
    settings = site.config.get('settings', {})
    collections = site.config.get('collections', {})

    global COLLECTIONS
    global COLLECTIONS_JSON
    for name, conf in collections.items():
        coll = Collection(conf['title'], conf['path'], conf['template'], site.path,
                          pages=site.pages(), config=site.config)
        order = conf.get('order')
        if order:
            coll.sort(**order)
        coll.create_navigation()
        COLLECTIONS[name] = coll
        COLLECTIONS_JSON[name] = coll.serialize()

    global NEWS_JSON
    NEWS_JSON = toDict(settings,
        COLLECTIONS['article'].filter('news', key='category'))

    global DEVELOPER_NEWS_JSON
    DEVELOPER_NEWS_JSON = toDict(settings,
        COLLECTIONS['article'].filter('developernews', key='category'))


def preBuildPage(site, page, context, data):
    """
    Add collections to every page context so we can
    access them from wherever on the site.
    """

    config = context['__CACTUS_SITE__'].config
    extra = {
        "CURRENT_PAGE": page,
        "CONFIG": config.get('settings', {}),
        # TODO: make this more generic!
        "news_json": NEWS_JSON,
        "developer_news_json": DEVELOPER_NEWS_JSON,
    }
    context.update(extra)

    for name, collection_json in COLLECTIONS_JSON.items():
        context[name+'_json'] = collection_json

    for name, collection in COLLECTIONS.items():
        context[name] = collection
        if collection.contains_page(page):
            ctx = collection.page_context(page)
            tpl = get_template(ctx.get('template', collection.template))
            raw = force_text(ctx[Collection.CONTEXT_RAW_KEY])
            ctx[Collection.CONTEXT_OUTPUT_KEY] = mark_safe(
                markdown(raw, extras=MARKDOWN_EXTRAS)
            )
            context.update(ctx)
            data = tpl.render(context)

    return context, data
