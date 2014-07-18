#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
class UnitTestException(UserWarning):
    def __init__(self, message):
        super(UnitTestException, self).__init__(message)
