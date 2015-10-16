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

import re
import hashlib
import logging

try:
    from StringIO import StringIO
except ImportError:
    # python 3
    from io import StringIO

from datetime import datetime
from markdown2 import markdown

from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)
HEADER_RE = r'(\w+)\:\s([\S\s]*)\n'


def toDict(conf, posts):
    site = conf.get('site', '')
    return [dict(
        id = hashlib.md5(x['url'].encode()).hexdigest(),
        title = x['title'],
        date = x['date'],
        tags = x['tags'],
        category = x['category'],
        permalink = '{0}{1}'.format(site, x['url']),
        content = u'',
        excerpt = Truncator(strip_tags(markdown(force_text(x['raw_body']), safe_mode=True))).words(25),
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

