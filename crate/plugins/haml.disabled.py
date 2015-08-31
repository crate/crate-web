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

import sys
import os
import codecs

# How to:
#     * Install hamlpy (https://github.com/jessemiller/HamlPy)
#     * .haml files will compiled to .html files


from hamlpy.hamlpy import Compiler
from cactus.utils.filesystem import fileList

CLEANUP = []

def preBuild(site):
    for path in fileList(site.paths['pages']):

        #only file ends with haml
        if not path.endswith('.haml'):
            continue

        #read the lines
        haml_lines = codecs.open(path, 'r', encoding='utf-8').read().splitlines()

        #compile haml to html
        compiler = Compiler()
        output = compiler.process_lines(haml_lines)

        #replace path
        outPath = path.replace('.haml', '.html')

        #write the html file
        with open(outPath,'w') as f:
            f.write(output)

        CLEANUP.append(outPath)


def postBuild(site):
    global CLEANUP
    for path in CLEANUP:
        print path
        os.remove(path)
    CLEANUP = []
