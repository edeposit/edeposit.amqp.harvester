#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from harvester.scrappers import autoparser


# Variables ===================================================================



# Functions & objects =========================================================
# with pytest.raises(AssertionError):

def test_create_dom():
    data = "<xe>x</xe>"

    dom = autoparser._create_dom(data)
    assert isinstance(dom, dhtmlparser.HTMLElement)

    assert dom.childs[0].parent is dom

    # html element from html element
    dom = autoparser._create_dom(dom)
    assert isinstance(dom, dhtmlparser.HTMLElement)
    assert dom.childs[0].parent is dom


def test_locate_element():
    data = "<xe>x</xe><xex>x</xex><xer>xx</xer>"
    dom = autoparser._create_dom(data)

    el = autoparser._locate_element(
        dom,
        "xx"
    )
    assert len(el) == 1
    assert el[0].isTag()
    assert el[0].getTagName() == "xer"
    assert el[0].getContent() == "xx"

    el = autoparser._locate_element(
        dom,
        "x"
    )
    assert len(el) == 2
    assert el[0].isTag()
    assert el[0].getTagName() == "xe"
    assert el[0].getContent() == "x"


def test_locate_element_transformer_param():
    data = "<xe>x</xe><xex>x</xex><xer>xx</xer>"
    dom = autoparser._create_dom(data)

    el = autoparser._locate_element(
        dom,
        "XX",
        lambda x: x.upper()
    )
    assert len(el) == 1
    assert el[0].isTag()
    assert el[0].getTagName() == "xer"
    assert el[0].getContent() == "xx"