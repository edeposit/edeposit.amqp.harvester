#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import unicodedata

import edeposit.amqp.aleph as aleph

# from .. import settings


# Variables ===================================================================



# Functions & objects =========================================================
def name_to_vector(name):
    """
    Convert `name` to the ASCII vector.

    Example:
        >>> name_to_vector("ing. Franta Putšálek")
        ['putsalek', 'franta', 'ing']

    Args:
        name (str): Name which will be vectorized.

    Returns:
        list: Vector created from name.
    """
    if not isinstance(name, unicode):
        name = name.decode("utf-8")

    name = name.lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    name = "".join(filter(lambda x: x.isalpha() or x == " ", list(name)))

    return sorted(name.split(), key=lambda x: len(x), reverse=True)


def compare_names(first, second):
    """
    Compare two names in complicated, but more error prone way.

    Algorithm is using vector comparison.

    Example:
        >>> compare_names("Franta Putšálek", "ing. Franta Putšálek")
        100.0
        >>> compare_names("F. Putšálek", "ing. Franta Putšálek")
        50.0

    Args:
        first (str): Fisst name as string.
        second (str): Second name as string.

    Returns:
        float: Percentage of the similarity.
    """
    first = name_to_vector(first)
    second = name_to_vector(second)

    zipped = zip(first, second)

    if not zipped:
        return 0

    similarity_factor = 0
    for fitem, sitem in zipped:
        if fitem == sitem:
            similarity_factor += 1

    return (float(similarity_factor) / len(zipped)) * 100


def filter_publication(publication):
    query = None
    isbn_query = False
    if publication.optionals and publication.optionals.ISBN:
        query = aleph.ISBNQuery(publication.optionals.ISBN)
        isbn_query = True
    else:
        query = aleph.TitleQuery(publication.title)

    result = aleph.reactToAMQPMessage(aleph.SearchRequest(query), "")

    if not result.records:
        return publication

    # if there was results with this ISBN, compare titles of the books
    # (sometimes, there are different books with same ISBN because of human
    # errors)
    if isbn_query:
        for record in result.records:
            epub = record.epublication

            if compare_names(epub.nazev, publication.title) >= 80:
                return None

        return publication

    # compare authors name
    for record in result.records:
        epub = record.epublication

