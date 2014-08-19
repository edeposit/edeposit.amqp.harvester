#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import os.path
import argparse

import yaml
import dhtmlparser

import utils


# Variables ===================================================================



# Functions & objects =========================================================
def read_config(file_name):
    with open(file_name) as f:
        return yaml.load_all(f.read())


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


def _find_common_root(elements):
    pass


def _collect_paths(elements):
    pass

def _filter_paths():
    pass


def select_best_paths(files):
    config = read_config(file)
    dom = _create_dom(dom)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Autoparser - parser generator."
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="""YAML Configuration file. This file is used to specify paths to
                data and matches, which will be used to create generator."""
    )

    args = parser.parse_args()

    if not os.path.exists(args.config):
        sys.stderr.write("Can't open '%s'!\n" % args.config)
        sys.exit(1)

    config = read_config(args.config)

    print select_best_paths(config)

