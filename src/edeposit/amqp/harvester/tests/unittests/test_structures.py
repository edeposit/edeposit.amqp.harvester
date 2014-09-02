#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from harvester.structures import Author, Optionals, Publication, Publications


# Functions & objects =========================================================
def test_author():
    name = "Franta Putšálek"
    a = Author(name)

    assert a.name == name
    assert a.URL is None

    a = Author(name, "url")

    assert a.name == name
    assert a.URL == "url"


def test_optionasl():
    o = Optionals()

    assert hasattr(o, "sub_title")
    assert hasattr(o, "format")
    assert hasattr(o, "pub_date")
    assert hasattr(o, "pub_place")
    assert hasattr(o, "ISBN")
    assert hasattr(o, "description")
    assert hasattr(o, "pages")
    assert hasattr(o, "EAN")
    assert hasattr(o, "language")
    assert hasattr(o, "edition")
    assert hasattr(o, "URL")
    assert hasattr(o, "binding")

    nto = o.to_namedtuple()

    assert hasattr(nto, "sub_title")
    assert hasattr(nto, "format")
    assert hasattr(nto, "pub_date")
    assert hasattr(nto, "pub_place")
    assert hasattr(nto, "ISBN")
    assert hasattr(nto, "description")
    assert hasattr(nto, "pages")
    assert hasattr(nto, "EAN")
    assert hasattr(nto, "language")
    assert hasattr(nto, "edition")
    assert hasattr(nto, "URL")
    assert hasattr(nto, "binding")


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
    assert nt.optionals.EAN == "xex"


def test_publications():
    p = Publications([1, 2])

    assert p.publications == [1, 2]
