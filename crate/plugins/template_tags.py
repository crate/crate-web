# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

from django.template.loader import add_to_builtins

# register filters
add_to_builtins('web.filters')
# register tags
add_to_builtins('web.tags')
