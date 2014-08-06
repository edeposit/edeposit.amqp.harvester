#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Utilities used in scrappers.
"""
# Imports =====================================================================
import dhtmlparser


# Functions & objects =========================================================
def _get_encoding(dom, default="utf-8"):
    """
    Try to look for meta tag in given `dom`.

    Args:
        dom (obj): pyDHTMLParser dom of HTML elements.
        default (default "utr-8"): What to use if encoding is not found in
                                   `dom`.

    Returns:
        str/default: Given encoding or `default` parameter if not found.
    """
    encoding = dom.find("meta", {"http-equiv": "Content-Type"})

    if not encoding:
        return default

    encoding = encoding[0].params.get("content", None)

    if not encoding:
        return default

    return encoding.lower().split("=")[-1]


def handle_encodnig(html):
    """
    Look for encoding in given `html`. Try to convert `html` to utf-8.

    Args:
        html (str): HTML code as string.

    Returns:
        str: HTML code encoded in UTF.
    """
    encoding = _get_encoding(
        dhtmlparser.parseString(
            html.split("</head>")[0]
        )
    )

    if encoding == "utf-8":
        return html

    return html.decode(encoding).encode("utf-8")


def get_first_content(el_list, alt=None, strip=True):
    """
    Return content of the first element in `el_list` or `alt`. Also return `alt`
    if the content string of first element is blank.

    Args:
        el_list (list): List of HTMLElement objects.
        alt (default None): Value returner when list or content is blank.
        strip (bool, default True): Call .strip() to content.

    Returns:
        str or alt: String representation of the content of the first element \
                    or `alt` if not found.
    """
    if not el_list:
        return alt

    content = el_list[0].getContent()

    if strip:
        content = content.strip()

    if not content:
        return alt

    return content


def is_absolute_url(url, protocol="http"):
    """
    Test whether `url` is absolute url (``http://domain.tld/something``) or
    relative (``../something``).

    Args:
        url (str): Tested string.
        protocol (str, default "http"): Protocol which will be seek at the
                 beginning of the `url`.

    Returns:
        bool: True if url is absolute, False if not.
    """
    if ":" not in url:
        return False

    protocol, rest = url.split(":", 1)

    if protocol.startswith(protocol) and rest.startswith("//"):
        return True

    return False


def normalize_url(base_url, rel_url):
    """
    Normalize the `url` - from relative, create absolute URL.

    Args:
        base_url (str): Domain with ``protocol://`` string
        rel_url (str): Relative or absolute url.

    Returns:
        str/None: Normalized URL or None if `url` is blank.
    """
    if not rel_url:
        return None

    if not is_absolute_url(rel_url):
        rel_url = base_url + rel_url.replace("../", "/")

    return rel_url
