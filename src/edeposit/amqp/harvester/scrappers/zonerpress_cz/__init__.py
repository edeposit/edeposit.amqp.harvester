#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import httpkie
import dhtmlparser

from .. import utils
from harvester import structures

import zonerpress_api as zapi


# Variables ===================================================================
BASE_URL = "http://www.zonerpress.cz"
BOOKS_URL = BASE_URL + "/knihy/?pageindex="
EBOOKS_URL = BASE_URL + "/elektronicke-knihy/?pageindex="
OTHER_PUBLISHERS_URL = BASE_URL + "/knihy-jinych-vydavatelu/?pageindex="
LINKS = [
    BOOKS_URL,
    EBOOKS_URL,
    OTHER_PUBLISHERS_URL
]

DOWNER = httpkie.Downloader()


# Functions & objects =========================================================
def _get_max_page(dom):
    div = dom.find("div", {"class": "razeniKnihListovani"})

    if not div:
        return 1

    # isolate only page numbers from links
    links = div[0].find("a")
    max_page = filter(
        lambda x: "href" in x.params and "pageindex=" in x.params["href"],
        links
    )
    max_page = map(
        lambda x: x.params["href"].split("pageindex=")[-1],
        max_page
    )
    max_page = filter(lambda x: x.isdigit(), max_page)
    max_page = map(lambda x: int(x), max_page)

    if not max_page:
        return 1

    return max(max_page)


def _parse_book_links(dom):
    links = []
    picker = lambda x: x.params.get("class", "").startswith("boxProKnihy")

    for el in dom.find(None, fn=picker):
        book_ref = el.find("a")

        if not book_ref or "href" not in book_ref[0].params:
            continue

        links.append(book_ref[0].params["href"])

    return links


def get_book_links(links):
    book_links = []

    for link in links:
        data = DOWNER.download(link + "1")
        dom = dhtmlparser.parseString(data)

        book_links.extend(_parse_book_links(dom))

        max_page = _get_max_page(dom)
        if max_page == 1:
            continue

        for i in range(max_page - 1):
            data = DOWNER.download(link + str(i + 2))

            book_links.extend(
                _parse_book_links(
                    dhtmlparser.parseString(data)
                )
            )

    return book_links


def _strip_content(el):
    content = el.getContent().strip()

    if content == "-":
        return None

    return content


def _parse_authors(authors):
    link = authors.find("a")
    link = link[0].params.get("href") if link else None

    author_list = _strip_content(authors)

    if "(" in author_list:
        author_list = author_list.split("(")[0]

    return map(
        lambda author: structures.Author(author.strip(), link),
        author_list.strip().split(",")
    )


def _process_book(link):
    data = DOWNER.download(link)
    dom = dhtmlparser.parseString(
        utils.handle_encodnig(data)
    )
    dhtmlparser.makeDoubleLinked(dom)

    pub = structures.Publication(
        title=_strip_content(zapi.get_title(dom)),
        authors=_parse_authors(zapi.get_author(dom)),
        price=_strip_content(zapi.get_price(dom)),
        publisher=_strip_content(zapi.get_publisher(dom))
    )

    pub.optionals.URL = link
    pub.optionals.pages = _strip_content(zapi.get_pages(dom))
    pub.optionals.pub_date = _strip_content(zapi.get_pub_date(dom))
    pub.optionals.ISBN = _strip_content(zapi.get_ISBN(dom))
    pub.optionals.binding = _strip_content(zapi.get_binding(dom))

    # post checks
    if pub.title.startswith("E-kniha:"):
        pub.title = pub.title.replace("E-kniha:", "", 1).strip()
        pub.optionals.is_ebook = True

    if " " in pub.optionals.ISBN:
        pub.optionals.ISBN = pub.optionals.ISBN.split(" ")[0]

    if "(" in pub.optionals.ISBN:
        pub.optionals.ISBN = pub.optionals.ISBN.split("(")[0]

    return pub


def get_publications():
    """
    Get list of publication offered by ben.cz.

    Returns:
        list: List of :class:`structures.Publication` objects.
    """
    books = []
    for link in get_book_links(LINKS):
        books.append(
            _process_book(link)
        )

        print books[0].to_namedtuple()
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
    zapi.test_parsers()
    return utils.self_test_idiom(get_publications)

print get_publications()