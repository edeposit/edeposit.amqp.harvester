#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


# Variables ===================================================================



# Functions & objects =========================================================
def _get_encoding(dom, default="utf-8"):
    encoding = dom.find("meta", {"http-equiv": "Content-Type"})

    if not encoding:
        return default

    if "content" not in encoding[0].params:
        return default

    encoding = encoding[0].params["content"]

    return encoding.lower().split("=")[-1]


def handle_encodnig(html):
    encoding = _get_encoding(
        dhtmlparser.parseString(
            html.split("</head>")[0]
        )
    )

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