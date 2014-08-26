#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import harvester.edeposit_autoparser as autoparser
from harvester.autoparser import vectors


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
def test_el_to_path_vector():
    dom = autoparser._create_dom(EXAMPLE_DATA)
    el = dom.find("container")

    assert el

    el = el[0]

    vector = vectors.el_to_path_vector(el)

    assert vector[0] == dom
    assert vector[1] == dom.find("root")[0]
    assert vector[2] == dom.find("xax")[0]
    assert vector[3] == el

    assert len(vector) == 4


def test_common_vector_root():
    v1 = [1, 2, 3, 4, 5]
    v2 = [1, 2, 8, 9, 0]

    assert vectors.common_vector_root(v1, v2) == [1, 2]


def test_find_common_root():
    dom = autoparser._create_dom(EXAMPLE_DATA)

    xax = dom.find("xax")[0]
    container = dom.find("container")[0]

    croot = vectors.find_common_root([xax, container])

    assert croot[0] == dom
    assert croot[1] == dom.find("root")[0]
    assert croot[2] == xax

    assert len(croot) == 3