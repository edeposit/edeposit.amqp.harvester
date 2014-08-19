#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


import utils


# Variables ===================================================================



# Functions & objects =========================================================
def read_config(files):
    pass


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
    return dom.find(
        None,
        fn=utils.content_matchs(el_content, transformer)
    )


def _match_elements(dom, matches):
    out = {}
    for key, content in matches.items():
        matching_elements = _locate_element(dom, content)

        if not matching_elements:
            raise UserWarning(
                "Can't locate element with content '%s'!" % content
            )

        if len(matching_elements) > 1:
            raise UserWarning(
                "Ambigious content '%s'!" % content
                + "Content was found in multiple elements!"
            )

        out[key] = matching_elements[0]

    return out


def _collect_paths(elements):
    pass

def _filter_paths():
    dom = _create_dom(dom)





def create_parser(input):
    pass