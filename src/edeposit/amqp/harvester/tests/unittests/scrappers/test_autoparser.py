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
EXAMPLE_DATA = """
    <root>
        something something
        <sometag>something something</sometag>
        <sometag>something something</sometag>
        <xax>
            something something
            <container>i wan't this</container>
        </xax>
        <sometag>something something</sometag>
        <container id="mycontent">and this</container>
        something something
    </root>
"""


# Functions & objects =========================================================
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


def test_match_elements():
    dom = autoparser._create_dom(EXAMPLE_DATA)
    matches = {
        "first": {
            "data": "i wan't this",
        },
        "second": {
            "data": "and this",
        }
    }

    matching_elements = autoparser._match_elements(dom, matches)

    assert matching_elements
    assert len(matching_elements) == 2

    assert matching_elements["first"]["data"].getContent() == matches["first"]["data"]
    assert matching_elements["second"]["data"].getContent() == matches["second"]["data"]


def test_match_elements_not_found():
    dom = autoparser._create_dom(EXAMPLE_DATA)
    matches = {
        "first": {
            "data": "notfound_data",
        }
    }

    with pytest.raises(UserWarning):
        autoparser._match_elements(dom, matches)


def test_match_elements_multiple_matches():
    dom = autoparser._create_dom(
        """
        <root>
            something something
            <sometag>something something</sometag>
            <sometag>something something</sometag>
            <xax>
                something something
                <container>azgabash</container>
            </xax>
            <sometag>something something</sometag>
            <container id="mycontent">azgabash</container>
            something something
        </root>
        """
    )

    matches = {
        "first": {
            "data": "azgabash",
        }
    }

    with pytest.raises(UserWarning):
        autoparser._match_elements(dom, matches)


def test_el_to_path_vector():
    dom = autoparser._create_dom(EXAMPLE_DATA)
    el = dom.find("container")

    assert el

    el = el[0]

    vector = autoparser._el_to_path_vector(el)

    assert vector[0] == dom
    assert vector[1] == dom.find("root")[0]
    assert vector[2] == dom.find("xax")[0]
    assert vector[3] == el

    assert len(vector) == 4
