#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


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

        self._any_set = False
        self._all_set = True

    def __setattr__(self, key, val):
        if "_all_set" in self.__dict__ and key not in self.__dict__:
            raise ValueError(
                "%s has no attribute %s!" % (self.__class__.__name__, key)
            )

        if not key.startswith("_") and key is not None:
            self.__dict__["_any_set"] = True

        self.__dict__[key] = val

    def to_namedtuple(self):
        keys = filter(lambda x: not x.startswith("_"), self.__dict__)
        opt_nt = namedtuple(self.__class__.__name__, keys)
        filtered_dict = dict(map(lambda x: (x, self.__dict__[x]), keys))

        return opt_nt(**filtered_dict)


class Publication(object):
    def __init__(self, title, author, pages, price, publisher):
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.publisher = publisher

        self.optionals = Optionals()

        self._all_set = True

    def to_namedtuple(self):
        keys = filter(lambda x: not x.startswith("_"), self.__dict__)
        opt_nt = namedtuple(self.__class__.__name__, keys)

        filt_dict = dict(map(lambda x: (x, self.__dict__[x]), keys))

        if filt_dict["optionals"]._any_set:
            filt_dict["optionals"] = filt_dict["optionals"].to_namedtuple()
        else:
            filt_dict["optionals"] = None

        return opt_nt(**filt_dict)

    def _get_hash(self):  # TODO: improve robustness of hashing
        return self.title + self.author

    def __setattr__(self, key, val):
        if "_all_set" in self.__dict__ and key not in self.__dict__:
            raise ValueError(
                "%s has no attribute %s!" % (self.__class__.__name__, key)
            )

        self.__dict__[key] = val

    def __hash__(self):
        return hash(self._get_hash())

    def __eq__(self, other):
        if not other:
            return False

        keys = filter(
            lambda x: not x.startswith("_") and x != "optionals",
            self.__dict__
        )

        for key in keys:
            if getattr(self, key) != getattr(other, key):
                return False

        return True
