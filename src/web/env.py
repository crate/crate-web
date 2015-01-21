# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import os
import sys
import json

if __name__ == '__main__':
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    conf = {}
    with open(os.path.join(BASE, 'config','local.json'), 'r') as fp:
        conf.update(json.load(fp))
    extra_path = os.path.join(BASE, 'config','{0}.json'.format(sys.argv[1]))
    if os.path.exists(extra_path):
        with open(extra_path, 'r') as fp:
            conf.update(json.load(fp))
    env = json.dumps(conf, indent=2)
    print(env)
