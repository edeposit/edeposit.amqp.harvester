#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & objects =========================================================
class NeighCall():
    def __init__(self, tag_name, params, fn_params):
        self.tag_name = tag_name
        self.params = params
        self.fn_params = fn_params


class PathCall(namedtuple("PathCall", ["call_type", "index", "params"])):
    pass


class Chained(object):
    def __init__(self, chain):
        # necesarry because of reversed() and other iterator-returning functions
        self.chain = list(chain)


def _params_or_none(params):
    return params if params else None


def _neighbour_to_path_call(neig_type, neighbour, element):
    params = [None, None, neighbour.getContent().strip()]

    if neighbour.isTag():
        params = [
            neighbour.getTagName(),
            _params_or_none(neighbour.params),
            neighbour.getContent().strip()
        ]

    return PathCall(
        neig_type + "_neighbour_tag",
        0,  # TODO: Dynamic lookup
        NeighCall(element.getTagName(), _params_or_none(element.params), params)
    )


def neighbours_pattern(element):
    # check if there are any neighbours
    if not element.parent:
        return []

    parent = element.parent

    # filter only visible tags/neighbours
    neighbours = filter(
        lambda x: x.isTag() and not x.isEndTag() or x.getContent().strip() \
                  or x is element,
        parent.childs
    )
    if len(neighbours) <= 1:
        return []

    output = []
    element_index = neighbours.index(element)

    # pick left neighbour
    if element_index >= 1:
        output.append(
            _neighbour_to_path_call(
                "left",
                neighbours[element_index - 1],
                element
            )
        )

    # pick right neighbour
    if element_index + 1 < len(neighbours):
        output.append(
            _neighbour_to_path_call(
                "right",
                neighbours[element_index + 1],
                element
            )
        )

    return output


def predecesors_pattern(element, root):
    """

    Returns:
        list: ``[PathCall()]` - list with one :class:`PathCall` object (to
              allow use with ``.extend(predecesors_pattern())``).
    """
    def is_root_container(el):
        return el.parent.parent.getTagName() == ""

    if not element.parent or not element.parent.parent or \
       is_root_container(element):
        return []

    trail = [
        [
            element.parent.parent.getTagName(),
            _params_or_none(element.parent.parent.params)
        ],
        [
            element.parent.getTagName(),
            _params_or_none(element.parent.params)
        ],
        [element.getTagName(), _params_or_none(element.params)],
    ]

    match = root.match(*trail)
    if element in match:
        return [
            PathCall("match", match.index(element), trail)
        ]
