# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

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
            name="Mathias Fußenegger",
            title="Core Developer",
            email="",
            ),
        dict(
            name="Christian Haudum",
            title="Integrations",
            email="",
            ),
        dict(
            name="Eugene Pustovit",
            title="Integrations",
            email="",
            ),
        dict(
            name="Spanky",
            title="aka Tom Kapanka Developer Advocate",
            email="",
            ),
        dict(
            name="Tyler Randles",
            title="Developer Evangelist",
            email="",
            ),
        dict(
            name="Chris Ward",
            title="Developer Advocate",
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
        ]

    return context, data
