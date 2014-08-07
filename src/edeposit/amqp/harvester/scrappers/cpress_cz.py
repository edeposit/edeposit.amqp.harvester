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


def _parse_authors(html_chunk):
    authors_tags = html_chunk.match(
        ["div", {"class": "polozka_autor"}],
        "a"
    )

    authors = []
    for author_tag in authors_tags:
        # get name
        name = author_tag.getContent().strip()

        # skip tags without name
        if not name:
            continue

        # get url - if not found, set it to None
        url = author_tag.params.get("href", None)
        if url:
            url = normalize_url(BASE_URL, url)

        authors.append(
            Author(name, url)
        )

    return authors


def _parse_price(html_chunk):
    price = html_chunk.find("span", {"class": "cena"})

    if not price:
        raise UserWarning("Price not found!")

    return get_first_content(price)


def _match_table(th_content):
    def _match_table_closure(element):
        # I need <tr> tag
        if element.getTagName() != "tr":
            return False

        # containing in first level of childs <th> tag
        th = element.match("th", absolute=True)
        if not th:
            return False

        # which's content match `th_content`
        if th[0].getContent() != th_content:
            return False

        # and also contains <td> tag
        if not element.match("td", absolute=True):
            return False

        return True

    return _match_table_closure


def _parse_ean(html_chunk):
    ean_tag = html_chunk.find("tr", fn=_match_table("EAN:"))

    if not ean_tag:
        return None

    return get_first_content(ean_tag[0].find("td"))


def _parse_date(html_chunk):
    pass


def _parse_format(html_chunk):
    pass


def _process_book(html_chunk):
    """
    Parse available informations about book from the book details page.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    # download page with details
    data = DOWNER.download(book_url)
    dom = dhtmlparser.parseString(
        handle_encodnig(data)
    )
    details = dom.find("div", {"id": "kniha_detail"})[0]

    # required parameters
    title, book_url = _parse_title_url(html_chunk)
    pub = Publication(
        title=title,
        authors=_parse_authors(html_chunk),
        price=_parse_price(details),
        publisher="CPress"
    )

    # optional parameters
    pub.optionals.URL = book_url


    return pub


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

# get_publications()