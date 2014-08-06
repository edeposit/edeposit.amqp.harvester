#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import httpkie
import dhtmlparser

from utils import handle_encodnig, get_first_content, normalize_url, has_param

from structures import Author
from structures import Publication

# from ..structures import Author
# from ..structures import Publication


# Variables ===================================================================
BASE_URL = "http://www.cpress.cz/"
URL = BASE_URL + "/novinky/"
DOWNER = httpkie.Downloader()


# Functions & objects =========================================================
def _parse_alt_title(html_chunk):
    title = html_chunk.find("img", fn=has_param("alt"))

    if not title:
        raise UserWarning("Can't find alternative title source!")

    return title[0].params["alt"].strip()


def _parse_alt_url(html_chunk):
    url_list = html_chunk.find("a", fn=has_param("href"))
    url_list = map(lambda x: x.params["href"], url_list)
    url_list = filter(lambda x: not x.startswith("autori/"), url_list)

    if not url_list:
        return None

    return normalize_url(BASE_URL, url_list[0])


def _parse_title_url(html_chunk):
    url = None
    title_tags = html_chunk.match(
        ["div", {"class": "polozka_nazev"}],
        ["a", None, has_param("href")]
    )

    if not title_tags:
        return _parse_alt_title(html_chunk), _parse_alt_url(html_chunk)

    title = title_tags[0]

    url = normalize_url(BASE_URL, title.params["href"])
    title = title.getContent()

    if not title:
        title = _parse_alt_title(html_chunk)

    return title, url



def _process_book(html_chunk):
    """
    Parse available informations about book from the book details page.

    Args:
        book_url (str): Absolute URL of the book.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    title = html_chunk.find("")

    # pub = Publication(
    #     title=title,
    #     authors=_parse_authors(html_chunk),
    #     pages=pages,
    #     price=_parse_price(html_chunk),
    #     publisher="Grada"
    # )


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

    book_list = dom.find("div", {"class": "polozka"})

    books = []
    for book in book_list:
        books.append(
            _process_book(book)
        )

    return books

get_publications()