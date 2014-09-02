#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from harvester import settings


# Functions & objects =========================================================
def test_settings_attributes():
    hasattr(settings, "USE_DUP_FILTER")
    hasattr(settings, "USE_ALEPH_FILTER")
    hasattr(settings, "ALEPH_FILTER_BY_AUTHOR")
    hasattr(settings, "DUP_FILTER_FILE")
