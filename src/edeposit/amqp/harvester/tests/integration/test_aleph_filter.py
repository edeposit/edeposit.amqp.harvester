#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.filters import aleph_filter
from harvester.structures import Publication


# Variables ===================================================================



# Functions & objects =========================================================
def test_filter_publication():
    p = Publication("ajksdhaklsjdh", "author", "pages", "price", "publisher")

    assert aleph_filter.filter_publication(p) == p  # not found

    # check lookup by book title
    p = Publication(
        "Umění programování v unixu",
        "random",
        "",
        "",
        ""
    )
    assert aleph_filter.filter_publication(p, cmp_authors=False) == None  # found

    # check lookup by title and authors name
    p = Publication(
        "Umění programování v unixu",
        "Raymond",  # !
        "",
        "",
        ""
    )
    assert aleph_filter.filter_publication(p) == None  # found

    # lookup by ISBN
    p = Publication(
        "",
        "",  # !
        "",
        "",
        ""
    )
    p.optionals.ISBN = "80-86056-31-7"
    assert aleph_filter.filter_publication(p) == p  # not found

    p.title = "Zen a umění internetu"
    assert aleph_filter.filter_publication(p) == None  # found

    # lookup by ISBN with typo in title
    p.title = "Zen a umění intrnetu"  # typo
    assert aleph_filter.filter_publication(p) == p  # not found
