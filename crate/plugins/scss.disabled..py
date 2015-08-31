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

import os
import sys
import pipes
import shutil
import subprocess

from cactus.utils.filesystem import fileList

"""
This plugin uses pyScss to translate sass files to css

Install:

sudo easy_install pyScss

"""

try:
	from scss import Scss
except:
	sys.exit("Could not find pyScss, please install: sudo easy_install pyScss")


CSS_PATH = 'static/css'

for path in fileList(CSS_PATH):

	if not path.endswith('.scss'):
		continue

	with open(path, 'r') as f:
		data = f.read()

	css = Scss().compile(data)

	with open(path.replace('.scss', '.css'), 'w') as f:
		f.write(css)
