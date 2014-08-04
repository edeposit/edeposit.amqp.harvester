#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Utilities used in scrappers.
"""
# Imports =====================================================================
import dhtmlparser


# Functions & objects =========================================================
def _get_encoding(dom, default="utf-8"):
    """
    Try to look for meta tag in given `dom`.

    Args:
        dom (obj): pyDHTMLParser dom of HTML elements.
        default (default "utr-8"): What to use if encoding is not found in
                                   `dom`.

    Returns:
        str/default: Given encoding or `default` parameter if not found.
    """
    encoding = dom.find("meta", {"http-equiv": "Content-Type"})

    if not encoding:
        return default

    encoding = encoding[0].params.get("content", None)

    if not encoding:
        return default

    return encoding.lower().split("=")[-1]


def handle_encodnig(html):
    """
    Look for encoding in given `html`. Try to convert `html` to utf-8.

    Args:
        html (str): HTML code as string.

    Returns:
        str: HTML code encoded in UTF.
    """
    encoding = _get_encoding(
        dhtmlparser.parseString(
            html.split("</head>")[0]
        )
    )

    if encoding == "utf-8":
        return html

    return html.decode(encoding).encode("utf-8")


def get_first_content(el_list, alt=None, strip=True):
    """
    Return content of the first element in `el_list` or `alt`. Also return `alt`
    if the content string of first element is blank.

    Args:
        el_list (list): List of HTMLElement objects.
        alt (default None): Value returner when list or content is blank.
        strip (bool, default True): Call .strip() to content.

    Returns:
        str or alt: String representation of the content of the first element \
                    or `alt` if not found.
    """
    if not el_list:
        return alt

    content = el_list[0].getContent()

    if strip:
        content = content.strip()

    if not content:
        return alt

    return content
