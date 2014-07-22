#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import traceback

import ben_cz


# Functions & objects =========================================================
def self_test_all():
    try:
        ben_cz.self_test()
    except Exception, e:
        raise UserWarning(
            e.message + "\n---\n" + traceback.format_exc().strip()
        )
