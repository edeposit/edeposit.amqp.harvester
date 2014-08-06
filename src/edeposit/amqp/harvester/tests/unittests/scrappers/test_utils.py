#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.scrappers import utils, grada_cz


# Functions & objects =========================================================
def test_normalize_url():
    assert utils.normalize_url(grada_cz.BASE_URL, "../xex") == grada_cz.BASE_URL + "/xex"
    assert utils.normalize_url(grada_cz.BASE_URL, "/xex") == grada_cz.BASE_URL + "/xex"
    assert utils.normalize_url(grada_cz.BASE_URL, "http://xerexe.com") == "http://xerexe.com"
