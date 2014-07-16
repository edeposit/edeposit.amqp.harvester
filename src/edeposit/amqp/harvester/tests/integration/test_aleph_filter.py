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
    p = Publication("title", "author", "pages", "price", "publisher")

    assert aleph_filter.filter_publication(p) == p

    p = Publication(
        "Umění programování v unixu",
        "author",
        "pages",
        "price",
        "publisher"
    )

    assert aleph_filter.filter_publication(p) is None
