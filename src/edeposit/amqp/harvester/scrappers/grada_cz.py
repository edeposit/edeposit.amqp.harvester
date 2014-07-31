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
BASE_URL = "http://www.grada.cz"
URL = BASE_URL + "/novinky/?start=0&krok=100"
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


def _normalize_url(url):
    if not url:
        return None

    if "http://" not in url:
        url = BASE_URL + url.replace("../", "/")

    return url


def _first_content(el_list, alt=None):
    if not el_list:
        return alt

    content = el_list[0].getContent()

    if not content:
        return alt

    return content


def _parse_alt_title(html_chunk):
    title = html_chunk.find(
        "input",
        {"src": "../images_buttons/objednat_off.gif"}
    )

    assert title, "Can't find alternative title!"
    assert "title" in title.params, "Can't find alternative title source!"

    return title.params["title"].split(":", 1)[-1]


def _parse_title_url(html_chunk):
    title = html_chunk.find("div", {"class": "comment"})

    if not title:
        return _parse_alt_title(html_chunk)

    title = title[0].find("h2")
    if not title:
        return _parse_alt_title(html_chunk)

    # look for the url of the book if present
    url = None
    url_tag = title[0].find("a")
    if url_tag:
        url = url_tag[0].params.get("href", None)
        title = url_tag

    return title[0].getContent(), _normalize_url(url)


def _parse_subtitle(html_chunk):
    subtitle = html_chunk.match(
        ["div", {"class": "comment"}],
        "h2",
        ["span", {"class": "gray"}],
    )

    return _first_content(subtitle)


def _process_book(html_chunk):
    # title, url = _parse_title_url(html_chunk)
    # authors = _parse_authors(html_chunk)
    # publisher = _parse_publisher(html_chunk)
    # price = _parse_price(html_chunk)
    # pages = _parse_pages(html_chunk)

    title, url = _parse_title_url(html_chunk)
    subtitle = _parse_subtitle(html_chunk)

    print title
    print url
    print subtitle
    print "---"


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
        books.append(
            _process_book(book)
        )

    return books


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