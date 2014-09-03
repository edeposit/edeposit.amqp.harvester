#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import httpkie
import dhtmlparser

from utils import handle_encodnig, get_first_content, normalize_url
from utils import self_test_idiom

from structures import Author
from structures import Publication

# from ..structures import Author
# from ..structures import Publication


# Variables ===================================================================
URL = "http://www.zonerpress.cz/inshop/robots/odberatele.xml"
DOWNER = httpkie.Downloader()


# Functions & objects =========================================================
def _parse_authors(html_chunk):
    pass


def _process_book(html_chunk):
    """
    Parse available informations about book from the book details page.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.


    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    # required informations
    pub = Publication(
        title=get_first_content(html_chunk.find("product")),
        authors=_parse_authors(html_chunk),
        price=get_first_content(html_chunk.find("price")),
        publisher="Grada"
    )


def get_publications():
    """
    Get list of publication offered by ben.cz.

    Returns:
        list: List of :class:`structures.Publication` objects.
    """
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(
        handle_encodnig(data)
    )

    books = []
    for book in dom.find("shopitem"):
        books.append(
            _process_book(book)
        )

        break

    return books


def self_test():
    """
    Perform basic selftest.

    Returns:
        True: When everything is ok.

    Raises:
        AssertionError: When there is some problem.
    """
    return self_test_idiom(get_publications)

print get_publications()