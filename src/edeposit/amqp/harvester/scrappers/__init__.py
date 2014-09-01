#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import ben_cz
import grada_cz
import cpress_cz


# Functions & objects =========================================================
def self_test_all():
    """
    Run tests on all submodules/scrappers.

    Raises:
        UserWarning: If one of the tests fails.
    """
    ben_cz.self_test()
    grada_cz.self_test()
    cpress_cz.self_test()
