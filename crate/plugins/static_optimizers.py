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

from cactus.contrib.external.closure import ClosureJSOptimizer
from cactus.contrib.external.yui import YUICSSOptimizer


def preBuild(site):
    """
    Registers optimizers as requested by the configuration.
    Be sure to read the plugin to understand and use it.
    """

    # Inspect the site configuration, and retrieve an `optimize` list.
    # This lets you configure optimization selectively.
    # You may want to use one configuration for staging with no optimizations, and one
    # configuration for production, with all optimizations.
    optimize = site.config.get("optimize", [])

    if "js" in optimize:
        # If `js` was found in the `optimize` key, then register our JS optimizer.
        # This uses closure, but you could use cactus.contrib.external.yui.YUIJSOptimizer!
        site.external_manager.register_optimizer(ClosureJSOptimizer)

    if "css" in optimize:
        # Same thing for CSS.
        site.external_manager.register_optimizer(YUICSSOptimizer)

    # Add your own types here!
