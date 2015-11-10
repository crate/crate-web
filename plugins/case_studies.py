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
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from web.utils import parseDate, parsePost

DIR = 'use-cases/case-studies/'
CASES = []

# https://github.com/trentm/python-markdown2/wiki/link-patterns
link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]

def filterCases(cases, categ):
    return filter(lambda x: categ in x.get('category'), cases)


def preBuild(site):

    global CASES

    # Build all the cases
    for case in site.pages():
        if case.path.startswith(DIR):

            # Skip non html cases for obvious reasons
            if not case.path.endswith('.html'):
                continue

            # Parse headers and markdown body
            headers, body = parsePost(case.data())

            # Build a context for each post
            caseContext = Context()
            caseContext.update(headers)
            caseContext['raw_body'] = body
            caseContext['path'] = case.path
            caseContext['date'] = parseDate(headers.get('date') or headers.get('created'))
            caseContext['url'] = case.absolute_final_url
            caseContext['tags'] = headers.get('tags') and [h.strip() for h in headers['tags'].split(',')] or []
            caseContext['category'] = headers.get('category') and [h.strip() for h in headers['category'].split(',')] or []
            CASES.append(caseContext)

    # Sort the cases by date
    CASES = sorted(CASES, key=lambda x: x['date'])
    CASES.reverse()

    indexes = range(0, len(CASES))

    for i in indexes:
        if i+1 in indexes: CASES[i]['prev_post'] = CASES[i+1]
        if i-1 in indexes: CASES[i]['next_post'] = CASES[i-1]


def preBuildPage(site, page, context, data):
    """
    Add the list of cases to every page context so we can
    access them from wherever on the site.
    """
    context['cases'] = CASES

    for case in CASES:
        if case['path'] == page.path:
            tpl = get_template(case.get('template', 'case-study.html'))
            raw = force_text(case['raw_body'])
            case['body'] = mark_safe(markdown(raw,
                extras=["fenced-code-blocks","header-ids"]))
            context['__CACTUS_CURRENT_PAGE__'] = page
            context['CURRENT_PAGE'] = page
            context.update(case)
            data = tpl.render(context)

    return context, data
