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

"""
This plugin uses glue to sprite images:
http://glue.readthedocs.org/en/latest/quickstart.html

Install:

(Only if you want to sprite jpg too)
brew install libjpeg

(Only if you want to optimize pngs with optipng)
brew install optipng

sudo easy_install pip
sudo pip uninstall pil
sudo pip install pil
sudo pip install glue
"""

try:
	import glue
except Exception, e:
	sys.exit('Could not use glue: %s\nMaybe install: sudo easy_install glue' % e)


IMG_PATH = 'static/img/sprites'
CSS_PATH = 'static/css/sprites'

KEY = '_PREV_CHECKSUM'

def checksum(path):
	command = 'md5 `find %s -type f`' % pipes.quote(IMG_PATH)
	return subprocess.check_output(command, shell=True)

def preBuild(site):

	currChecksum = checksum(IMG_PATH)
	prevChecksum = getattr(site, KEY, None)

	# Don't run if none of the images has changed
	if currChecksum == prevChecksum:
		return

	if os.path.isdir(CSS_PATH):
		shutil.rmtree(CSS_PATH)

	os.mkdir(CSS_PATH)
	os.system('glue --cachebuster --crop --optipng "%s" "%s" --project' % (IMG_PATH, CSS_PATH))

	setattr(site, KEY, currChecksum)
