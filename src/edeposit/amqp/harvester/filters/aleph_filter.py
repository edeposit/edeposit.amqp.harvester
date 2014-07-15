#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from .. import settings

import edeposit.amqp.aleph as aleph


# Variables ===================================================================



# Functions & objects =========================================================
def filter(publication):
    query = None
    isbn_query = False
    if publication.optionals and publication.optionals.ISBN:
        query = aleph.ISBNQuery(publication.optionals.ISBN)
        isbn_query = True
    else:
        query = aleph.TitleQuery(publication.title)

    result = aleph.reactToAMQPMessage(aleph.SearchRequest(query, ""))

    if not result.records:
        return publication

    # TODO: filter by author name
    if not isbn_query:
        pass

