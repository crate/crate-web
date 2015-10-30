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

def preBuildPage(site, page, context, data):
    """
    Add the list of posts to every page context so we can
    access them from wherever on the site.
    """
    context['team'] = [
        dict(
            name="Jodok Batlogg",
            title="Founder, CEO",
            email="",
            ),
        dict(
            name="Christian Lutz",
            title="Founder, COO",
            email="",
            ),
        dict(
            name="Bernd Dorn",
            title="Founder, CTO",
            email="",
            ),
        dict(
            name="Chris Chabot",
            title="Head of Developer Relations",
            email="",
            ),
        dict(
            name="Michael Beer",
            title="Developer Integrations",
            email="",
            ),
        dict(
            name="Philipp Bogensberger",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Julia Bundschuh",
            title="Executive Assistant",
            email="",
            ),
        dict(
            name="Sarah Fischli",
            title="Project Management",
            email="",
            ),
        dict(
            name="Jacob Fisher",
            title="Developer Relations",
            email="",
            ),
        dict(
            name="Mathias Fußenegger",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Christian Haudum",
            title="Developer Integrations",
            email="",
            ),
        dict(
            name="Ruslan Kovalov",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Johannes Moser",
            title="Product Owner, Scrum Master",
            email="",
            ),
        dict(
            name="Sebastian Utz",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Matthias Wahl",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Chris Ward",
            title="Developer Advocate",
            email="",
            ),
        ]

    return context, data
