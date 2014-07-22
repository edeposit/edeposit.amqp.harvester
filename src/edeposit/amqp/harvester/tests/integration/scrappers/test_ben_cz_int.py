#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester.scrappers import ben_cz


# Functions & objects =========================================================
def test_module():
    assert ben_cz.self_test()
