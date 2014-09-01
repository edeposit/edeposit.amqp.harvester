#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import copy
import os.path
import tempfile

import pytest

import harvester.autoparser.conf_reader as conf_reader


# Variables ===================================================================
example_data = {
    'html': 'http://google.com',
    'first': {
        'required': True,
        'data': "i wan't this",
        'notfoundmsg': "Can't find variable '$name'."
    },
    'second': {
        'data': 'and this'
    },
}
yaml_data = """
html: http://google.com
first:
    data: i wan't this
    required: true
    notfoundmsg: Can't find variable '$name'.
second:
    data: and this
---
html: http://google.com
first:
    data: i wan't this
"""


# Functions & objects =========================================================
def structure_test(proc_data, original_data):
    assert "<html" in proc_data["html"].lower()
    assert proc_data["link"] == original_data["html"]
    assert proc_data["vars"]
    assert proc_data["vars"]["first"]["required"]
    assert proc_data["vars"]["first"]["notfoundmsg"] == "Can't find variable 'first'."
    assert proc_data["vars"]["second"]

    original_data["html"] = "azgabash"


def test_get_source():
    content = "somecontent"
    filename = None

    try:
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write(content)
            filename = f.name

        assert conf_reader._get_source(filename) == content
    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

    with pytest.raises(UserWarning):
        conf_reader._get_source("/azgabash")

    assert "html" in conf_reader._get_source("http://google.com")


def test_process_config_item():
    test_data = copy.deepcopy(example_data)
    out = conf_reader._process_config_item(test_data, ".")

    structure_test(out, test_data)

    with pytest.raises(UserWarning):
        conf_reader._process_config_item(test_data, ".")


def test_read_config():
    filename = None
    try:
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write(yaml_data)
            filename = f.name

        structure_test(
            conf_reader.read_config(filename)[0],
            example_data
        )
    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)
