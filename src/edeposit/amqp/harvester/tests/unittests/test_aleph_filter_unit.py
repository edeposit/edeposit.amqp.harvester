#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.filters import aleph_filter


# Functions & objects =========================================================
def test_name_to_vector():
    name = aleph_filter.name_to_vector("Franta Putšálek")
    assert name == ["putsalek", "franta"]

    name = aleph_filter.name_to_vector("ing. Franta Putšálek")
    assert name == ["putsalek", "franta", "ing"]

    name1 = aleph_filter.name_to_vector("Franta Putšálek")
    name2 = aleph_filter.name_to_vector("Putšálek Franta")

    assert name1 == name2


def test_compare_names():
    cn = aleph_filter.compare_names("Franta Putšálek", "Putšálek Franta")
    assert cn == 100.0

    cn = aleph_filter.compare_names("Franta Putšálek", "Putšálek Pepa")
    assert cn == 50.0

    cn = aleph_filter.compare_names("ing. Franta Putšálek", "Putšálek Franta")
    assert cn == 100.0

    cn = aleph_filter.compare_names("Tonda Otruba", "Putšálek Franta")
    assert cn == 0
