#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser

from harvester.autoparser import path_patterns


# Variables ===================================================================



# Functions & objects =========================================================
def test_PathCall():
    params = ["type", "index", "params"]
    p = path_patterns.PathCall(*params)

    assert p.call_type == params[0]
    assert p.index == params[1]
    assert p.params == params[2]


def test_Chained():
    c = path_patterns.Chained((1, 2, 3))

    # test conversion to list
    assert c.chain == [1, 2, 3]


def test_params_or_none():
    assert path_patterns._params_or_none({}) is None
    assert path_patterns._params_or_none({1:2}) == {1:2}


def test_neighbour_to_path_call():
    dom = dhtmlparser.parseString("<xex>\tHello   </xex>")
    xex = dom.find("xex")[0]

    res = path_patterns._neighbour_to_path_call("left", xex)

    assert isinstance(res, path_patterns.PathCall)
    assert res.call_type == "left_neighbour_tag"
    assert res.index == 0
    assert res.params == ["xex", None, "Hello"]


def test_neighbour_to_path_call_text():
    dom = dhtmlparser.parseString("<xex>\tHello   </xex>")
    text = dom.find("xex")[0].childs[0]

    res = path_patterns._neighbour_to_path_call("left", text)

    assert isinstance(res, path_patterns.PathCall)
    assert res.call_type == "left_neighbour_tag"
    assert res.index == 0
    assert res.params == [None, None, "Hello"]


def test_neighbours_pattern():
    pass


def test_predecesors_pattern():
    pass