#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import uuid
import os.path

from harvester import settings
from harvester.filters import dup_filter
from harvester.structures import Publication


# Variables ===================================================================
DATA = {"prvni", "druhy", "treti"}


# Functions & objects =========================================================
def test_save_cache():
    settings.DUP_FILTER_FILE = "/tmp/" + str(uuid.uuid4())
    reload(dup_filter)

    dup_filter.save_cache(DATA)

    assert os.path.exists(settings.DUP_FILTER_FILE)


def test_load_cache():
    data = dup_filter.load_cache()

    assert isinstance(data, set)

    assert "prvni" in data
    assert "druhy" in data
    assert "treti" in data


def test_deduplicate():
    p = Publication("title", "author", "pages", "price", "publisher")

    assert dup_filter.filter_publication(p) == p
    assert dup_filter.filter_publication(p) is None
    assert dup_filter.filter_publication(p) is None


def teardown_module():
    os.remove(settings.DUP_FILTER_FILE)
