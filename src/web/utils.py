# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import re
import hashlib
import logging

from StringIO import StringIO
from datetime import datetime
from markdown2 import markdown

from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)
HEADER_RE = r'(\w+)\:\s([\S\s]*)\n'


def toDict(conf, posts):
    site = conf.get('site', '')
    return [dict(
        id = hashlib.md5(x['url']).hexdigest(),
        title = x['title'],
        date = x['date'],
        tags = x['tags'],
        category = x['category'],
        permalink = '{0}{1}'.format(site, x['url']),
        content = u'',
        excerpt = Truncator(strip_tags(markdown(force_unicode(x['raw_body']), safe_mode=True))).words(25),
        author = x['author'],
    ) for x in posts]

def parseDate(date_str=None):
    if date_str and re.match(r'^\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}$', date_str):
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    elif date_str and re.match(r'^\d{4}\-\d{2}\-\d{2}', date_str):
        return datetime.strptime(date_str, '%Y-%m-%d')
    elif date_str and re.match(r'^\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}', date_str):
        return datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    logger.warning("Date format not correct, should be 'yyyy-mm-dd', 'yyyy-mm-ddThh:mm' or 'yyyy/mm/dd hh:mm:ss'\n{0}".format(date_str))
    return datetime.now()


def parsePost(post):
    headers = {}
    fn = StringIO(post.data())
    for line in fn:
        res = re.match(HEADER_RE, line)
        if res:
            header, value = res.groups()
            headers[header.lower()] = value
        else:
            break
    body = fn.read()
    return (headers, body)

