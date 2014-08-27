#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser

from harvester.autoparser import path_patterns


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

    res = path_patterns._neighbour_to_path_call("left", xex, xex)

    assert isinstance(res, path_patterns.PathCall)
    assert res.call_type == "left_neighbour_tag"
    assert res.index == 0
    assert res.params.tag_name == "xex"
    assert res.params.params == None
    assert res.params.fn_params == ["xex", None, "Hello"]


def test_neighbour_to_path_call_text():
    dom = dhtmlparser.parseString("<xex>\tHello   </xex>")
    text = dom.find("xex")[0].childs[0]

    res = path_patterns._neighbour_to_path_call("left", text, text)

    assert isinstance(res, path_patterns.PathCall)
    assert res.call_type == "left_neighbour_tag"
    assert res.index == 0
    assert res.params.tag_name == "\tHello   "
    assert res.params.params == None
    assert res.params.fn_params == [None, None, "Hello"]


def test_neighbours_pattern():
    dom = dhtmlparser.parseString(
        """
        asd
        <x>haxaxex</x>
        <xex>\tHello</xex>
        <xep></xep>
        asd
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    xex = dom.find("xex")[0]
    res = path_patterns.neighbours_pattern(xex)

    assert res
    assert len(res) == 2

    left, right = res

    assert left.call_type == "left_neighbour_tag"
    assert left.index == 0
    assert left.params.tag_name == "xex"
    assert left.params.params == None
    assert left.params.fn_params == ["x", None, "haxaxex"]

    assert right.call_type == "right_neighbour_tag"
    assert right.index == 0
    assert right.params.tag_name == "xex"
    assert right.params.params == None
    assert right.params.fn_params == ["xep", None, ""]


def test_neighbours_pattern_text_neigh():
    dom = dhtmlparser.parseString(
        """
        asd
        <xex>\tHello</xex>
        <xep></xep>
        asd
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    xex = dom.find("xex")[0]
    res = path_patterns.neighbours_pattern(xex)

    assert res
    assert len(res) == 2

    left, right = res

    assert left.call_type == "left_neighbour_tag"
    assert left.index == 0
    assert res[0].params.tag_name == "xex"
    assert res[0].params.params == None
    assert left.params.fn_params == [None, None, "asd"]

    assert right.call_type == "right_neighbour_tag"
    assert right.index == 0
    assert res[0].params.tag_name == "xex"
    assert res[0].params.params == None
    assert right.params.fn_params == ["xep", None, ""]


def test_neighbours_pattern_left_corner():
    dom = dhtmlparser.parseString(
        """
        <xex>\tHello</xex>
        <xep></xep>
        asd
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    xex = dom.find("xex")[0]
    res = path_patterns.neighbours_pattern(xex)

    assert res
    assert len(res) == 1

    assert res[0].call_type == "right_neighbour_tag"
    assert res[0].index == 0
    assert res[0].params.tag_name == "xex"
    assert res[0].params.params == None
    assert res[0].params.fn_params == ["xep", None, ""]


def test_neighbours_pattern_right_corner():
    dom = dhtmlparser.parseString(
        """
        asd
        <xex>\tHello</xex>
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    xex = dom.find("xex")[0]
    res = path_patterns.neighbours_pattern(xex)

    assert res
    assert len(res) == 1

    assert res[0].call_type == "left_neighbour_tag"
    assert res[0].index == 0
    assert res[0].params.tag_name == "xex"
    assert res[0].params.params == None
    assert res[0].params.fn_params == [None, None, "asd"]


def test_neighbours_pattern_both_corners():
    dom = dhtmlparser.parseString(
        """
        <xex>\tHello</xex>
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    xex = dom.find("xex")[0]
    res = path_patterns.neighbours_pattern(xex)

    assert not res


def test_predecesors_pattern():
    dom = dhtmlparser.parseString(
        """
        <root>
            <xex>
                <x>content</x>
            </xex>
        </root>
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    x = dom.find("x")[0]

    res = path_patterns.predecesors_pattern(x, dom)

    assert res
    assert len(res) == 1

    assert isinstance(res[0], path_patterns.PathCall)

    assert res[0].call_type == "match"
    assert res[0].index == 0
    assert res[0].params == [
        ["root", None],
        ["xex", None],
        ["x", None],
    ]


def test_predecesors_pattern_shallow_root():
    dom = dhtmlparser.parseString(
        """
        <root>
            <x>content</x>
        </root>
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    x = dom.find("x")[0]

    res = path_patterns.predecesors_pattern(x, dom)

    assert not res
