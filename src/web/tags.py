# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

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

