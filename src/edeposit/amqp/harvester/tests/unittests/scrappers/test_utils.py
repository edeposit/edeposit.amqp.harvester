#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from harvester.scrappers import utils, grada_cz
from harvester.structures import Publication


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
    <blank id="xex" class="xax"> </blank>
    <xex>
        <bleh>asd</bleh>
        <ppp>content </ppp>
    </xex>
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


def test_get_first_content():
    dom = dhtmlparser.parseString(SAUCE)
    contents = dom.find("container")

    assert utils.get_first_content(contents) == contents[0].getContent().strip()
    assert utils.get_first_content([]) == None

    blank = dom.find("blank")
    assert utils.get_first_content(blank) == None

    assert utils.get_first_content([], alt=1) == 1
    assert utils.get_first_content(blank, alt=1, strip=False) == " "


def test_is_absolute_url():
    assert utils.is_absolute_url("http://xex")
    assert utils.is_absolute_url("https://xex")
    assert utils.is_absolute_url("ftp://xex", protocol="ftp")
    assert not utils.is_absolute_url("/hello")
    assert not utils.is_absolute_url("../hello")


def test_normalize_url():
    assert utils.normalize_url(grada_cz.BASE_URL, "../xex") == grada_cz.BASE_URL + "/xex"
    assert utils.normalize_url(grada_cz.BASE_URL, "/xex") == grada_cz.BASE_URL + "/xex"
    assert utils.normalize_url(grada_cz.BASE_URL, "http://xerexe.com") == "http://xerexe.com"


def test_has_param():
    dom = dhtmlparser.parseString(SAUCE)
    result = dom.find(None, fn=utils.has_param("class"))

    assert result
    assert result[0].getTagName() == "blank"


def test_must_contain():
    dom = dhtmlparser.parseString(SAUCE)

    cont = dom.find(None, fn=utils.must_contain("ppp", "content ", "bleh"))
    assert cont[0] == dom.find("xex")[0]


def test_content_matchs():
    dom = dhtmlparser.parseString(SAUCE)
    el = dom.find(None, fn=utils.content_matchs("i want this"))

    assert el
    assert el[0].getTagName() == "container"


def test_self_test_idiom():
    assert utils.self_test_idiom(
        lambda: [
            Publication("xex", [], "3", "garda"),
            Publication("xex", [], "3", "garda")
        ]
    )

    with pytest.raises(AssertionError):
        pub = Publication("xex", [], "3", "garda")
        pub.optionals.ISBN = "80-8605"

        utils.self_test_idiom(
            lambda: [
                pub,
                Publication("xex", [], "3", "garda")
            ]
        )

    with pytest.raises(AssertionError):
        pub = Publication("xex", [], "3", "garda")
        pub.optionals.URL = "ftp://xexex"

        utils.self_test_idiom(
            lambda: [
                pub,
                Publication("xex", [], "3", "garda")
            ]
        )
