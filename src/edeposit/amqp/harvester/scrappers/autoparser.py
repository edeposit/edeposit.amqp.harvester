#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


import utils


# Variables ===================================================================



# Functions & objects =========================================================
def _create_dom(dom):
    if not isinstance(dom, dhtmlparser.HTMLElement):
        dom = dhtmlparser.parseString(dom)

    dhtmlparser.makeDoubleLinked(dom)

def _locate_elements(dom):
    pass


def _collect_paths(dom, matches):
    dom = _create_dom(dom)

    for key, match in matches:
        pass



def create_parser(input):
    pass