#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from harvester.structures import Publication


# Functions & objects =========================================================
def test_publication():
    p = Publication("title", "author", "pages", "price", "publisher")

    # test properties of the Publication object
    assert p.title == "title"
    assert p.author == "author"
    assert p.pages == "pages"
    assert p.price == "price"
    assert p.publisher == "publisher"

    # test immutability of object, but mutability of properties
    with pytest.raises(ValueError):
        p.xax = 1
    p.price = 1
    assert p.price == 1

    # test properties of generated namedtuple
    nt = p.to_namedtuple()
    assert nt.title == "title"
    assert nt.author == "author"
    assert nt.pages == "pages"
    assert nt.price == 1
    assert nt.publisher == "publisher"

    assert nt.optionals is None

    # test that optionals can prevent setting themself to None if anything is
    # set in them
    p.optionals.ean = "xex"
    nt = p.to_namedtuple()
    assert nt.optionals is not None
    nt.optionals.ean == "xex"
