#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.scrappers import grada_cz


# Functions & objects =========================================================
def test_module():
    assert grada_cz.self_test()
