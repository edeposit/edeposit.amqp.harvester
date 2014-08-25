#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import copy
import os.path
import argparse

import dhtmlparser

import autoparser
import autoparser.utils as utils
import autoparser.conf_reader as conf_reader
import autoparser.vectors as vectors
import autoparser.path_patterns as path_patterns


# Functions & objects =========================================================
def _create_dom(data):
    """
    Creates doublelinked DOM from `data`.

    Args:
        data (str/HTMLElement): Either string or HTML element.

    Returns:
        obj: HTMLElement containing double linked DOM.
    """
    if not isinstance(data, dhtmlparser.HTMLElement):
        data = dhtmlparser.parseString(data)

    dhtmlparser.makeDoubleLinked(data)

    return data


def _locate_element(dom, el_content, transformer=None):
    """
    Find element containing `el_content` in `dom`. Use `transformer` function
    to content of all elements in `dom` in order to correctly transforming them
    to match them with `el_content`.

    Args:
        dom (obj): HTMLElement tree.
        el_content (str): Content of element will be picked from `dom`.
        transformer (fn, default None): Transforming function.

    Note:
        `transformer` parameter can be for example simple lambda::

            lambda x: x.strip()

    Returns:
        list: Matching HTMLElements.
    """
    return dom.find(
        None,
        fn=utils.content_matchs(el_content, transformer)
    )


def _match_elements(dom, matches):
    """
    Find location of elements matching patterns specified in `matches`.

    Args:
        dom (obj): HTMLElement DOM tree.
        matches (dict): Structure: ``{"var": {"data": "match", ..}, ..}``.

    Returns:
        dict: Structure: ``{"var": {"data": HTMLElement_obj, ..}, ..}``
    """
    out = {}
    for key, content in matches.items():
        matching_elements = _locate_element(
            dom,
            content["data"],
            transformer=lambda x: x.strip()
        )

        not_found_msg = "Can't locate element with content '%s'!" % key
        if content.get("notfoundmsg"):
            not_found_msg = content.get("notfoundmsg").replace("$name", key)

        if not matching_elements:
            raise UserWarning(not_found_msg)

        if len(matching_elements) > 1:
            raise UserWarning(
                "Ambigious content '%s'!" % content
                + "Content was found in multiple elements!"
            )

        out[key] = matching_elements[0]

    return out


_reversed = reversed  # jsem na Déro robot!
reversed = lambda sequence: list(_reversed(sequence))


def _collect_paths(element):  #TODO: test
    output = []

    # look for element by parameters - sometimes the ID is unique
    path = vectors.el_to_path_vector(element)
    root = path[0]
    params = element.params if element.params else None
    match = root.find(element.getTagName(), params)

    if len(match) == 1:
        output.append(
            ("find", 0, [element.getTagName(), params])
        )

    # look for element by neighbours
    output.extend(path_patterns.neighbours_pattern(element))

    # look for elements by patterns - element, which parent has tagname, and
    # which parent has tagname ..
    output.extend(path_patterns.predecesors_pattern(element, root))

    # look for element by paths from root to element
    index_backtrack = []
    last_index_backtrack = []
    params_backtrack = []
    last_params_backtrack = []

    for el in reversed(path):
        # skip root elements
        if not el.parent:
            continue

        tag_name = el.getTagName()
        match = el.parent.wfind(tag_name).childs
        index = match.index(el)

        index_backtrack.append(
            ("wfind", index, tag_name)
        )
        last_index_backtrack.append(
            ("wfind", index - len(match), tag_name)
        )

        # if element has some parameters, use them for lookup
        if el.params:
            match = el.parent.wfind(tag_name, el.params).childs
            index = match.index(el)

            params_backtrack.append(
                ("wfind", index, [tag_name, el.params])
            )
            last_params_backtrack.append(
                ("wfind", index - len(match), [tag_name, el.params])
            )
        else:
            params_backtrack.append(
                ("wfind", index, tag_name)
            )
            last_params_backtrack.append(
                ("wfind", index - len(match), tag_name)
            )

    output.extend([
        reversed(params_backtrack),
        reversed(last_params_backtrack),
        reversed(index_backtrack),
        reversed(last_index_backtrack),
    ])

    return output


def _working_path(dom, path):  #TODO: test
    """
    Check whether the path is working or not.
    """
    pass


def _filter_paths(matches, paths):
    pass


def select_best_paths(config):  #TODO: test
    possible_paths = {}

    # get list of all possible paths to all existing variables
    for example in config:
        dom = _create_dom(example["html"])
        matching_elements = _match_elements(dom, example["vars"])

        for key, match in matching_elements.items():
            if key not in possible_paths:  # TODO: merge paths together?
                possible_paths[key] = _collect_paths(match)

    # filter only paths, that works in all examples
    print possible_paths



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Autoparser - parser generator."
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="""YAML Configuration file used to specify paths to data and
                matches, which will be used to create generator."""
    )

    args = parser.parse_args()

    if not os.path.exists(args.config):
        sys.stderr.write("Can't open '%s'!\n" % args.config)
        sys.exit(1)

    config = conf_reader.read_config(args.config)

    if not config:
        sys.stderr.write("Configuration file '%s' is blank!\n" % args.config)
        sys.exit(1)

    print select_best_paths(config)
