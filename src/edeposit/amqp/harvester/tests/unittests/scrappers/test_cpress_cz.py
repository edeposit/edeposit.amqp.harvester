#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from harvester.scrappers import cpress_cz


# Variables ===================================================================



# Functions & objects =========================================================
def test_parse_alt_title():
    dom = dhtmlparser.parseString("""
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        </div>
    """
    )

    alt_title = cpress_cz._parse_alt_title(dom)

    assert alt_title == "Záhadná jízda králů"


def test_parse_alt_title_not_found():
    dom = dhtmlparser.parseString("""
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        </div>
    """
    )

    with pytest.raises(UserWarning):
        cpress_cz._parse_alt_title(dom)


def test_parse_alt_title_param_not_found():
    dom = dhtmlparser.parseString("""
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        </div>
    """
    )

    with pytest.raises(UserWarning):
        cpress_cz._parse_alt_title(dom)

