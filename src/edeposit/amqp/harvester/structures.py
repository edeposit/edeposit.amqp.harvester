#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================



# Functions & objects =========================================================
class Optionals(object):
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


class Publication(object):
    def __init__(self, title, author, pages, price, publisher):
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.publisher = publisher

        self.optionals = Optionals()
