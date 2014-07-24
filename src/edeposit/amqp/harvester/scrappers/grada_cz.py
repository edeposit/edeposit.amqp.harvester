#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import httpkie
import dhtmlparser

from structures import Author
from structures import Publication

# from ..structures import Author
# from ..structures import Publication


# Variables ===================================================================
URL = "http://www.grada.cz/novinky/?start=0&krok=100"
DOWNER = httpkie.Downloader()


# Functions & objects =========================================================
def _get_encoding(dom, default="utf-8"):
    encoding = dom.find("meta", {"http-equiv": "Content-Type"})

    if not encoding:
        return default

    if "content" not in encoding[0].params:
        return default

    encoding = encoding[0].params["content"]

    return encoding.lower().split("=")[-1]


def _handle_encodnig(html):
    encoding = _get_encoding(
        dhtmlparser.parseString(
            html.split("</head>")[0]
        )
    )

    return html.decode(encoding).encode("utf-8")


def get_publications():
    """
    Get list of publication offered by ben.cz.

    Returns:
        list: List of :class:`structures.Publication` objects.
    """
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(
        _handle_encodnig(data)
    )

    book_list = dom.find("div", {"class": "item"})

    books = []
    for book in book_list:
        print book
        print "--"


def self_test():
    """
    Perform basic selftest.

    Returns:
        True: When everything is ok.

    Raises:
        AssertionError: When there is some problem.
    """
    pass


get_publications()