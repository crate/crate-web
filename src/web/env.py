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
