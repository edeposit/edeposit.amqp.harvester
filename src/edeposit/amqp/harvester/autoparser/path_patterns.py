#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & objects =========================================================
class PathCall(namedtuple("PathCall", ["call_type", "index", "params"])):
    pass


class Chained(object):
    def __init__(self, chain):
        # necesarry because of reversed() and other iterator-returning functions
        self.chain = list(chain)


def _params_or_none(params):
    return params if params else None


def neighbours_pattern(element):  #TODO: test
    def neighbour_to_path_call(neig_type, neighbour):
        if neighbour.isTag():
            return PathCall(
                neig_type + "_neighbour_tag",
                0,
                [
                    neighbour.getTagName(),
                    _params_or_none(neighbour.params),
                    neighbour.getContent().strip()
                ]
            )

        return PathCall(
            neig_type + "_neighbour_tag",
            0,
            [None, None, neighbour.getContent().strip()]
        )

    # check if there are any neighbours
    if not element.parent or len(element.parent.childs) <= 1:
        return []

    parent = element.parent

    # filter only visible tags/neighbours
    neighbours = filter(
        lambda x: x.isTag() or x.getContent().strip() or x is element,
        parent.childs
    )
    if len(neighbours) <= 1:
        return []

    element_index = neighbours.index(element)
    output = []

    # pick left neighbour
    if element_index >= 1:
        output.append(
            neighbour_to_path_call("left", neighbours[element_index - 1])
        )

    # pick right neighbour
    if element_index + 2 < len(neighbours):
        output.append(
            neighbour_to_path_call("right", neighbours[element_index + 2])
        )

    return output


def predecesors_pattern(element, root):
    """

    Returns:
        list: ``[PathCall()]` - list with one :class:`PathCall` object (to
              allow use with ``.extend(predecesors_pattern())``).
    """
    if not element.parent or not element.parent.parent:
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
