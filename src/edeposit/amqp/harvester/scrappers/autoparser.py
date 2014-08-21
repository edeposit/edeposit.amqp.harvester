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

import yaml
import httpkie
import dhtmlparser

import utils


# Variables ===================================================================



# Functions & objects =========================================================
def _process_config_item(item):  #TODO: test
    """
    Process one item from the configuration file, which contains multiple items
    saved as dictionary.

    This function reads additional data from the config and do some
    replacements - for example, if you specify url, it will download data
    from this url and so on.

    Args:
        item (dict): Item, which will be processed.

    Note:
        Returned data format::
            {
                "html": "html code from file/url",
                "vars": {
                    "varname": {
                        "data": "matching data..",
                        ...
                    }
                }
            }

    Returns:
        dict: Dictionary in format showed above.
    """
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


def read_config(file_name):  #TODO: test
    """
    Read YAML file with configuration and pointers to example data.

    Args:
        file_name (str): Name of the file, where the configuration is stored.

    Returns:
        dict: Parsed and processed data (see :func:`_process_config_item`).

    Example YAML file::
        html: simple_xml.xml
        first:
            data: i wan't this
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: and this
        ---
        html: simple_xml2.xml
        first:
            data: something wanted
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: another wanted thing
    """
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
    out = copy.deepcopy(matches)

    for key, content in out.items():
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

    return out


def _el_to_path_vector(el):  #TODO: test
    path = [el]

    while el:
        path.append(el.parent)
        el = el.parent

    return reversed(path)


def common_vector_root(vec1, vec2):  #TODO: test
    root = []
    for v1, v2 in zip(vec1, vec2):
        if v1 == v2:
            root.append(v1)
        else:
            return root

    return root


def _find_common_root(elements):  #TODO: test
    if not elements:
        raise UserWarning("Can't find common root - no elements suplied.")

    root_path = _el_to_path_vector(elements.pop())

    for el in elements:
        el_path = _el_to_path_vector(el)

        root_path = common_vector_root(root_path, el_path)

        if not root_path:
            raise UserWarning("Vectors without common root:\n%s" % str(el_path))

    return root_path


def _collect_paths(elements):  #TODO: test
    pass


def _filter_paths():  #TODO: test
    pass


def select_best_paths(config):  #TODO: test
    first = config.pop(0)

    dom = _create_dom(first["html"])
    matching_elements = _match_elements(dom, first["vars"])

    # optimization - don't do all operations from document root, but from
    # the common root of all elements, which may be smaller
    only_elements = map(
        lambda (key, val): val["data"],
        matching_elements.items()
    )

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

