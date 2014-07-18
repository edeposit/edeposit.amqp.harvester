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
    price = details.find("td", {"id": "ctl00_ContentPlaceHolder1_TableCell10"})

    if not price:
        return None

    return price[0].getContent().strip()


def _process_book(book_url):
    data = DOWNER.download(book_url)
    dom = dhtmlparser.parseString(data)

    details = dom.find("div", {"id": "contentDetail"})

    assert details, "Can't find details of the book."

    details = details[0]

    # parse required informations

    # print details

    # print _parse_title(dom, details)
    # print _parse_authors(details)
    # print _parse_publisher(details)
    # print _parse_price(details)


    # pub = Publication(title, author, pages, price, publisher)


def parse_publications():
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(data)

    book_list = dom.find("div", {"class": "seznamKniha"})

    assert book_list, "Can't find <div> with class 'seznamKniha'!"

    for html_chunk in book_list[4:]:
        a = html_chunk.find("a")

        assert a, "Can't find link to the details of the book!"


        _process_book(a[0].params["href"])

        break

def self_test():
    pass

parse_publications()