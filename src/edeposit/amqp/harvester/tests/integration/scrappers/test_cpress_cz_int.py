#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.scrappers import cpress_cz


# Functions & objects =========================================================
def test_module():
    assert cpress_cz.self_test()
