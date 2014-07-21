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
URL = "http://shop.ben.cz/"
URL += r"Produkty.aspx?lang=cz&nak=BEN+-+technick%u00e1+literatura"
DOWNER = httpkie.Downloader()
DOWNER.cookies = {
    "shop.ben.cz": {
        "pageSize": "100",
        "viewProductSize": "tabulka"
    }
}


# Functions & objects =========================================================
def _get_last_td(el):
    """
    Return last <td> found in `el` DOM.

    Args:
        el (obj): :class:`dhtmlparser.HTMLElement` instance.

    Returns:
        obj: HTMLElement instance if found, or None if there are no <td> tags.
    """
    if not el:
        return None

    last = el[0].find("td")

    if not last:
        return None

    return last[-1]


def _get_td_or_none(details, ID):
    """
    Get <tr> tag with given `ID` and return last <td> tag from it's content.

    Args:
        details (obj): :class:`dhtmlparser.HTMLElement` instance.
        ID (str): id property of the <tr> tag.

    Returns:
        obj: HTMLElement contaning pointer to last <td> tag or None.
    """
    content = details.find("tr", {"id": ID})
    content = _get_last_td(content)

    # if content is None, return it
    if not content:
        return None

    content = content.getContent().strip()

    # if content is blank string, return None
    if not content:
        return None

    return content


# Parsers =====================================================================
def _parse_title(dom, details):
    title = details.find("h1")

    # if the header is missing, try to parse title from the <title> tag
    if not title:
        title = dom.find("title")
        assert title, "Can't find <title> tag!"

        return title[0].getContent().split("|")[0].strip()

    return title[0].getContent().strip()


def _parse_authors(details):
    authors = details.find(
        "tr",
        {"id": "ctl00_ContentPlaceHolder1_tblRowAutor"}
    )

    if not authors:
        return None  # book with unspecified authors

    # parse authors from HTML and convert them to Author objects
    author_list = []
    for author in authors[0].find("a"):
        author_obj = Author(author.getContent())

        if "href" in author.params:
            author_obj.URL = author.params["href"]

        author_list.append(author_obj)

    return author_list


def _parse_publisher(details):
    publisher = details.find(
        "td",
        {"id": "ctl00_ContentPlaceHolder1_TableCell3"}
    )

    # publisher is not specified
    if not publisher:
        return None

    publisher = dhtmlparser.removeTags(publisher[0]).strip()

    # return None instead of blank string
    if not publisher:
        return None

    return publisher


def _parse_price(details):
    price = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowBeznaCena"
    )

    return price


def _parse_pages_binding(details):
    pages = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowRozsahVazba"
    )

    if not pages:
        return None, None

    binding = None  # binding info and number of pages is stored in same string
    if "/" in pages:
        binding = pages.split("/")[1].strip()
        pages = pages.split("/")[0].strip()

    return pages, binding


def _parse_ISBN_EAN(details):
    isbn_ean = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowIsbnEan"
    )

    if not isbn_ean:
        return None, None

    ean = None
    isbn = None
    if "/" in isbn_ean:  # ISBN and EAN are stored in same string
        isbn, ean = isbn_ean.split("/")
        isbn = isbn.strip()
        ean = ean.strip()
    else:
        isbn = isbn_ean.strip()

    return isbn, ean


def _parse_edition(details):
    edition = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowVydani"
    )

    return edition


def _parse_description(details):
    description = details.find("div", {"class": "detailPopis"})

    # description not found
    if not description:
        return None

    # remove links to ebook version
    ekniha = description[0].find("div", {"class": "ekniha"})
    if ekniha:
        ekniha[0].replaceWith(dhtmlparser.HTMLElement(""))

    # remove links to other books from same cathegory
    detail = description[0].find("p", {"class": "detailKat"})
    if detail:
        detail[0].replaceWith(dhtmlparser.HTMLElement(""))

    # remove all HTML elements
    description = dhtmlparser.removeTags(description[0]).strip()

    # description is blank
    if not description:
        return None

    return description


def _process_book(book_url):
    """
    Parse available informations about book from the book details page.

    Args:
        book_url (str): Absolute URL of the book.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    data = DOWNER.download(book_url)
    dom = dhtmlparser.parseString(data)

    details = dom.find("div", {"id": "contentDetail"})

    assert details, "Can't find details of the book."

    details = details[0]

    # parse required informations
    title = _parse_title(dom, details)
    authors = _parse_authors(details)
    publisher = _parse_publisher(details)
    price = _parse_price(details)
    pages, binding = _parse_pages_binding(details)

    pub = Publication(
        title,
        authors,
        pages,
        price,
        publisher
    )

    # parse optional informations
    pub.optionals.url = book_url
    pub.optionals.binding = binding

    pub.optionals.ISBN, pub.optionals.EAN = _parse_ISBN_EAN(details)
    pub.optionals.edition = _parse_edition(details)
    pub.optionals.description = _parse_description(details)

    return pub


def parse_publications():
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(data)

    book_list = dom.find("div", {"class": "seznamKniha"})

    assert book_list, "Can't find <div> with class 'seznamKniha'!"

    for html_chunk in book_list[4:]:  # TODO: remove
        a = html_chunk.find("a")

        assert a, "Can't find link to the details of the book!"

        _process_book(a[0].params["href"])

        break  # TODO: remove

def self_test():
    pass

parse_publications()
