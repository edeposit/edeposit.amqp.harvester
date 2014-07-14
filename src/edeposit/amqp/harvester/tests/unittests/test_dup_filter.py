#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import uuid

from harvester import settings
from harvester.filters import dup_filter


# Functions & objects =========================================================
def test_save_cache():
    settings.DUP_FILTER_FILE = "/tmp/" + str(uuid.uuid4())
    reload(dup_filter)


def test_load_cache():
    c = dup_filter.load_cache()

    assert isinstance(c, set)


def test_deduplicate():
    pass
