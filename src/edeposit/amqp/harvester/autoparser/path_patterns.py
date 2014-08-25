#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & objects =========================================================
def _params_or_none(params):
    return params if params else None


def neighbours_pattern(element):  #TODO: test
    def neighbour_to_params(neig_type, neighbour):
        neighbour_data = None
        if neighbour.isTag():
            neighbour_data = (
                neig_type + "_neighbour_tag",
                0,
                [
                    neighbour.getTagName(),
                    _params_or_none(neighbour.params),
                    neighbour.getContent().strip()
                ]
            )
        else:
            neighbour_data = (
                neig_type + "_neighbour_tag",
                0,
                [None, None, neighbour.getContent().strip()]
            )

        return neighbour_data

    # check if there are any neighbours
    if not element.parent or len(element.parent.childs) <= 1:
        return []

    parent = element.parent
    neighbours = parent.childs
    element_index = neighbours.index(element)

    output = []
    neighbour = None

    # pick left neighbour
    if element_index >= 1:
        output.append(
            neighbour_to_params("left", neighbours[element_index - 1])
        )

    # pick right neighbour
    if element_index < len(neighbours) - 2:
        output.append(
            neighbour_to_params("right", neighbours[element_index + 1])
        )

    return output


def predecesors_pattern(element, root):
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
            ("match", match.index(element), trail)
        ]
