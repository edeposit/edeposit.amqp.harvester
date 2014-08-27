#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser

from harvester.autoparser import utils


# Variables ===================================================================
SAUCE = """
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
def test_is_equal_tag():
    dom = dhtmlparser.parseString(SAUCE)
    container = dom.find("container")[0]

    assert utils.is_equal_tag(container, "container", None, "i wan't this")
    assert not utils.is_equal_tag(container, "container", None, "xxx")
    assert utils.is_equal_tag(container, "container", None, None)
    assert not utils.is_equal_tag(container, "container", None, "")
    assert not utils.is_equal_tag(container, "xxx", None, "i wan't this")
    assert not utils.is_equal_tag(container, "xxx", None, None)
    assert utils.is_equal_tag(container, "", None, None)


def test_has_neigh():
    dom = dhtmlparser.parseString(SAUCE)
    dhtmlparser.makeDoubleLinked(dom)

    el = dom.find(
        "container",
        None,
        fn=utils.has_neigh(None, None, "something something", left=False)
    )

    assert el
    assert len(el) == 1

    assert el[0].getContent() == "and this"