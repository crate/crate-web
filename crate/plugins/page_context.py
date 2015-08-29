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

def preBuildPage(page, context, data):
    """
    Updates the context of the page to include: the page itself as {{ CURRENT_PAGE }}
    """

    # This will run for each page that Cactus renders.
    # Any changes you make to context will be passed to the template renderer for this page.

    extra = {
        "CURRENT_PAGE": page,
        # Add your own dynamic context elements here!
    }

    context.update(extra)
    return context, data
