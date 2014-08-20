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
import httpkie
import dhtmlparser

import utils


# Variables ===================================================================



# Functions & objects =========================================================
def _process_config_item(item):
    html = item.get("html", None)

    if not html:
        raise UserWarning("Can't find HTML source for item:\n%s" % str(item))

    # process HTML link
    if html.startswith("http://") or html.startswith("https://"):
        down = httpkie.Downloader()
        html = down.download(html)
    elif os.path.exists(html):
        with open(html) as f:
            html = f.read()
    else:
        raise UserWarning("html: '%s' is neither URL or data!" % html)

    del item["html"]
    return {
        "html": html,
        "vars": item
    }


def read_config(file_name):
    dirname = os.path.dirname(file_name)

    config = []
    with open(file_name) as f:
        os.chdir(dirname)
        for item in yaml.load_all(f.read()):
            config.append(
                _process_config_item(item)
            )

    return config


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

        content["data"] = matching_elements[0]

    return matches


def _find_common_root(elements):
    pass


def _collect_paths(elements):
    pass

def _filter_paths():
    pass


def select_best_paths(config):
    first = config.pop(0)

    dom = _create_dom(first["html"])
    matching_elements = _match_elements(dom, first["vars"])

    return matching_elements



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

    if not config:
        sys.stderr.write("Configuration file '%s' is blank!\n" % args.config)
        sys.exit(1)

    print select_best_paths(config)

