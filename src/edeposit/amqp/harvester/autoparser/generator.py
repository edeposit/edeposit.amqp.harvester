#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import inspect

import utils
import conf_reader
import path_patterns


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


# parser template generators ##################################################
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


def _neigh_template(parameters, index, left=True, required=False,
                                                  notfoundmsg=None):
    fn_string = "has_neigh(%s, left=%s)" % (
        repr(parameters.fn_params)[1:-1],
        repr(left)
    )

    output = IND + "el = dom.find(\n"
    output += IND + IND + "%s,\n" % repr(parameters.tag_name)

    if parameters.params:
        output += IND + IND + "%s,\n" % repr(parameters.params)

    output += IND + IND + "fn=%s\n" % fn_string
    output += IND + ")\n\n"

    if required:
        return output + _required_idiom(index, notfoundmsg)

    return output + _index_idiom("el", index)

# /parser template generators #################################################


def _get_parser_name(var_name):
    return "get_%s" % var_name


def _generate_parser(name, path, required=False, notfoundmsg=None):
    output = "def %s(dom):\n" % _get_parser_name(name)

    print path

    parser_table = {
        "find": lambda path:
            _find_template(path.params, path.index, required, notfoundmsg),
        "wfind": lambda path:
            _wfind_template(path.params, path.index, required, notfoundmsg),
        "match": lambda path:
            _match_template(path.params, path.index, required, notfoundmsg),
        "left_neighbour_tag": lambda path:
            _neigh_template(
                path.params,
                path.index,
                True,
                required,
                notfoundmsg
            ),
        "right_neighbour_tag": lambda path:
            _neigh_template(
                path.params,
                path.index,
                False,
                required,
                notfoundmsg
            ),
    }

    if isinstance(path, path_patterns.PathCall):
        output += parser_table[path.call_type](path)
    elif isinstance(path, path_patterns.Chained):
        for path in path.chain:
            output += parser_table[path.call_type](path)
    else:
        raise UserWarning(
            "Unknown type of path parameters! (%s)" % str(path)
        )

    output += IND + "return el\n"
    output += "\n"

    return output


def _unittest_template(config):
    output = "def test_parsers():\n"

    links = dict(map(lambda x: (x["link"], x["vars"]), config))

    for link in links.keys():
        output += IND + "# Test parsers against %s\n" % link
        output += IND + "html = handle_encodnig(_get_source(%s))\n" % repr(link)
        output += IND + "dom = dhtmlparser.parseString(html)\n\n"

        for var in links[link]:
            output += IND + "%s = %s(dom)\n" % (var, _get_parser_name(var))
            output += IND + "assert %s.getContent().strip() == %s.strip()" % (
                var,
                repr(links[link][var]["data"])
            )
            output += "\n\n"

    return output


def generate_parsers(config, paths):
    output = """#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
import httpkie
import dhtmlparser


# Utilities
"""
    # add source of neighbour picking functions from utils.py
    output += inspect.getsource(conf_reader._get_source) + "\n"
    output += inspect.getsource(utils._get_encoding) + "\n"
    output += inspect.getsource(utils.handle_encodnig) + "\n"
    output += inspect.getsource(utils.is_equal_tag) + "\n"
    output += inspect.getsource(utils.has_neigh) + "\n"
    output += "\n# Generated parsers\n\n"

    for name, path in paths.items():
        path = path[-1]  # pick path with highest priority

        required = config[0]["vars"][name].get("required", False)
        notfoundmsg = config[0]["vars"][name].get("notfoundmsg", "")

        output += _generate_parser(name, path, required, notfoundmsg)

    output += "\n# Unittest\n\n"
    output += _unittest_template(config)

    return output
