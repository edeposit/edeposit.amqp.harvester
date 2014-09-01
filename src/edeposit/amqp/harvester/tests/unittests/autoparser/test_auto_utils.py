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
        <container>i want this</container>
    </xax>
    <sometag>something something</sometag>
    <container id="mycontent">and this</container>
    something something
</root>
"""


# Functions & objects =========================================================
def test_get_encoding():
    content = """
    asdasd
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    asdasd
    """

    dom = dhtmlparser.parseString(content)
    assert utils._get_encoding(dom) == "utf-8"


def test_content_matchs():
    dom = dhtmlparser.parseString(SAUCE)
    el = dom.find(None, fn=utils.content_matchs("i want this"))

    assert el
    assert el[0].getTagName() == "container"


def test_is_equal_tag():
    dom = dhtmlparser.parseString(SAUCE)
    container = dom.find("container")[0]

    assert utils.is_equal_tag(container, "container", None, "i want this")
    assert not utils.is_equal_tag(container, "container", None, "xxx")
    assert utils.is_equal_tag(container, "container", None, None)
    assert not utils.is_equal_tag(container, "container", None, "")
    assert not utils.is_equal_tag(container, "xxx", None, "i want this")
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
