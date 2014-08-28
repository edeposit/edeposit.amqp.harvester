#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================
IND = "    "


# Functions & objects =========================================================
def _index_idiom(el_name, index, alt=None):
    el_index = "%s[%d]" % (el_name, index)

    if index == 0:
        cond = "%s" % el_name
    else:
        cond = "len(%s) - 1 >= %d" % (el_name, index)

    output = IND + "# pick element from list\n"

    return output + IND + "%s = %s if %s else %s\n\n" % (
        el_name,
        el_index,
        cond,
        repr(alt)
    )


def _required_idiom(index, notfoundmsg):
    cond = ""
    if index > 0:
        cond = " or len(el) - 1 < %d" % index

    output = IND + "if not el%s:\n" % cond
    output += IND + IND + "raise UserWarning(%s)\n\n" % repr(notfoundmsg)

    return output + IND + "el = el[%d]\n\n" % index


def _find_template(parameters, index, required=False, notfoundmsg=None):
    output = IND + "el = dom.find(%s)\n\n" % repr(parameters)[1:-1]

    if required:
        return output + _required_idiom(index, notfoundmsg)

    return output + _index_idiom("el", index)


def _wfind_template(parameters, index, required=False, notfoundmsg=None):
    output = IND + "el = dom.wfind(%s).childs\n\n" % repr(parameters)[1:-1]

    if required:
        return output + _required_idiom(index, notfoundmsg)

    return output + _index_idiom("el", index)


def _match_template(parameters, index, required=False, notfoundmsg=None):
    output = IND + "el = dom.match(%s)\n\n" % repr(parameters)[1:-1]

    #TODO: reduce None parameters

    if required:
        return output + _required_idiom(index, notfoundmsg)

    return output + _index_idiom("el", index)


def _generate_parser(name, path, required=False, notfoundmsg=None):
    output = "def get_%s(dom):\n" % name

    parser_table = {
        "find": lambda path:
            _find_template(path.params, path.index, required, notfoundmsg),
        "wfind": lambda path:
            _wfind_template(path.params, path.index, required, notfoundmsg),
        "match": lambda path:
            _match_template(path.params, path.index, required, notfoundmsg),
    }
    if path.call_type not in parser_table: #TODO: chained
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
        notfoundmsg = config[0]["vars"][name].get("notfoundmsg", "")

        output += _generate_parser(name, path, required, notfoundmsg)

    return output
