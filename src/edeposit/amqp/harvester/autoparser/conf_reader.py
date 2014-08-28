#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

import yaml
import httpkie


# Functions & objects =========================================================
def _process_config_item(item):  #TODO: test
    """
    Process one item from the configuration file, which contains multiple items
    saved as dictionary.

    This function reads additional data from the config and do some
    replacements - for example, if you specify url, it will download data
    from this url and so on.

    Args:
        item (dict): Item, which will be processed.

    Note:
        Returned data format::
            {
                "html": "html code from file/url",
                "vars": {
                    "varname": {
                        "data": "matching data..",
                        ...
                    }
                }
            }

    Returns:
        dict: Dictionary in format showed above.
    """
    html = item.get("html", None)

    if not html:
        raise UserWarning("Can't find HTML source for item:\n%s" % str(item))

    # process HTML link
    if html.startswith("http://") or html.startswith("https://"):
        down = httpkie.Downloader()
        html = down.download(html)
    elif os.path.exists(html):
        with open(html) as f:
            html = f.read()
    else:
        raise UserWarning("html: '%s' is neither URL or data!" % html)

    for key, val in item.items():
        if "notfoundmsg" in val:
            val["notfoundmsg"] = val["notfoundmsg"].replace("$name", key)

    del item["html"]
    return {
        "html": html,
        "vars": item
    }


def read_config(file_name):  #TODO: test
    """
    Read YAML file with configuration and pointers to example data.

    Args:
        file_name (str): Name of the file, where the configuration is stored.

    Returns:
        dict: Parsed and processed data (see :func:`_process_config_item`).

    Example YAML file::
        html: simple_xml.xml
        first:
            data: i wan't this
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: and this
        ---
        html: simple_xml2.xml
        first:
            data: something wanted
            required: true
            notfoundmsg: Can't find variable $name.
        second:
            data: another wanted thing
    """
    dirname = os.path.dirname(file_name)

    config = []
    with open(file_name) as f:
        os.chdir(dirname)
        for item in yaml.load_all(f.read()):
            config.append(
                _process_config_item(item)
            )

    return config
