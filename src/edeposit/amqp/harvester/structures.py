#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Variables ===================================================================



# Functions & objects =========================================================
class Optionals(namedtuple("Optionals", ["sub_title", "format", "pub_date",
                                         "pub_place", "ISBN", "description",
                                         "ean", "language"])):
    def __init__(self):
        self.sub_title = None
        self.format = None
        self.pub_date = None
        self.pub_place = None
        self.ISBN = None
        self.description = None
        self.ean = None
        self.language = None

    def __setattr__(self, attr, val):
        if attr not in self.__dict__:
            raise KeyError("%s is not allowed optional!" % attr)

        self.__dict__[attr] = val


class Publication(namedtuple("Publication", ["title", "author", "pages",
                                             "price", "publisher"])):
    def __init__(self, title, author, pages, price, publisher):
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.publisher = publisher

        self.optionals = Optionals()

    def __setattr__(self, attr, val):
        if attr not in self.__dict__:
            setattr(self.optionals, attr, val)

        self.__dict__[attr] = val
