#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================
IND = "    "


# Functions & objects =========================================================
def _find_template(parameters, index, required=False, notfound_msg=None):
    output = IND + "el = dom.find(%s)\n\n" % repr(parameters)[1:-1]

    if required:
        output += IND + "if not el:\n"
        output += IND + IND + "raise UserWarning(%s)\n\n" % repr(notfound_msg)

    return output


def _generate_parser(name, path, required=False, notfound_msg=None):
    output = "def get_%s(dom):\n" % name

    parser_table = {
        "find": lambda path:
            _find_template(path.params, path.index, required, notfound_msg),
    }
    if path.call_type not in parser_table:
        return ""

    output += parser_table[path.call_type](path)

    output += IND + "return el\n"
    output += "\n"

    return output


def generate_parsers(config, paths):
    output = ""

    for name, path in paths.items():
        path = path[0]  # pick path with highest priority

        required = config[0]["vars"][name].get("required", False)
        notfound_msg = config[0]["vars"][name].get("notfoundmsg", "")

        output += _generate_parser(name, path, required, notfound_msg)

    return output
