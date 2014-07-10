#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================



# Functions & objects =========================================================
class Publication(object):
    def __init__(self, title, author, pages, price, publisher):
        # required
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.publisher = publisher

        # optional
        self.sub_title = None
        self.format = None
        self.pub_date = None
        self.pub_place = None
        self.ISBN = None
        self.description = None
        self.ean = None
        self.language = None

        self.used_optionals = []

    @property
    def sub_title(self, val):
        self.sub_title = val

        if "sub_title" not in self.used_optionals:
            self.used_optionals.append("sub_title")

    @property
    def format(self, val):
        self.format = val

        if "format" not in self.used_optionals:
            self.used_optionals.append("format")

    @property
    def pub_date(self, val):
        self.pub_date = val

        if "pub_date" not in self.used_optionals:
            self.used_optionals.append("pub_date")

    @property
    def pub_place(self, val):
        self.pub_place = val

        if "pub_place" not in self.used_optionals:
            self.used_optionals.append("pub_place")

    @property
    def ISBN(self, val):
        self.ISBN = val

        if "ISBN" not in self.used_optionals:
            self.used_optionals.append("ISBN")

    @property
    def description(self, val):
        self.description = val

        if "description" not in self.used_optionals:
            self.used_optionals.append("description")

    @property
    def ean(self, val):
        self.ean = val

        if "ean" not in self.used_optionals:
            self.used_optionals.append("ean")

    @property
    def language(self, val):
        self.language = val

        if "language" not in self.used_optionals:
            self.used_optionals.append("language")



# Main program ================================================================
if __name__ == '__main__':
    pass
