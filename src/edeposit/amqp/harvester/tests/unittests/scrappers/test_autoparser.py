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



