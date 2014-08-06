#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from harvester.structures import Publication, Author


# Functions & objects =========================================================
def test_publication():
    p = Publication("title", [Author("author")], "price", "publisher")

    # test properties of the Publication object
    assert p.title == "title"
    assert p.authors[0].name == "author"
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
    assert nt.authors[0].name == "author"
    assert nt.price == 1
    assert nt.publisher == "publisher"

    assert nt.optionals is None

    # test that optionals can prevent setting themself to None if anything is
    # set in them
    p.optionals.EAN = "xex"
    nt = p.to_namedtuple()
    assert nt.optionals is not None
    nt.optionals.EAN == "xex"
