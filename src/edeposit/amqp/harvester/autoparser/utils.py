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


def has_param(param):
    """
    Generate function, which will check `param` is in html element.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def has_param_closure(element):
        """
        Look for `param` in `element`.
        """
        if element.params.get(param, "").strip():
            return True

        return False

    return has_param_closure


def must_contain(tag_name, tag_content, container_tag_name):
    """
    Generate function, which checks if given element contains `tag_name` with
    string content `tag_content` and also another tag named
    `container_tag_name`.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def must_contain_closure(element):
        # containing in first level of childs <tag_name> tag
        matching_tags = element.match(tag_name, absolute=True)
        if not matching_tags:
            return False

        # which's content match `tag_content`
        if matching_tags[0].getContent() != tag_content:
            return False

        # and also contains <container_tag_name> tag
        if container_tag_name and \
           not element.match(container_tag_name, absolute=True):
            return False

        return True

    return must_contain_closure


def content_matchs(tag_content, content_transformer=None):
    """
    Generate function, which checks whether the content of the tag matchs
    `tag_content`.

    Args:
        tag_content (str): Content of the tag which will be matched thru whole
                           DOM.
        content_transformer (fn, default None): Function used to transform all
                            tags before matching.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def content_matchs_closure(element):
        if not element.isTag():
            return False

        cont = element.getContent()
        if content_transformer:
            cont = content_transformer(cont)

        return tag_content == cont

    return content_matchs_closure


def has_neigh(tag_name, params=None, content=None, left=True):
    def neigh_match(element):
        if tag_name and tag_name != element.getTagName():
            return False

        if params and element.containsParamSubset(params):
            return False

        if content and content.strip() != element.getContent().strip():
            return False

        return True

    def has_neigh_closure(element):
        if not element.parent:
            return False

        # childs = []
        # if not (tag_name and params):
        childs = element.parent.childs
        # else:
            # childs = filter(lambda x: x.isTag(), element.parent.childs)

        # filter only visible tags/neighbours
        childs = filter(
            lambda x: x.isTag() or x.getContent().strip() or x is element,
            childs
        )
        if len(childs) <= 1:
            return False

        ioe = childs.index(element)
        if left and ioe > 0:
            return neigh_match(childs[ioe - 1])
        elif not left and ioe + 1 < len(childs):
            return neigh_match(childs[ioe + 1])

        return False

    return has_neigh_closure