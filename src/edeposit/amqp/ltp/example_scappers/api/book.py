#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# self xml-serialization class v1.0.0 (29.03.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 
# Unported License (http://creativecommons.org/licenses/by-nc-sa/3.0/cz/).
# Created in §Editor text editor.
#
# Notes:
    # 
import dhtmlparser as d

class Book:
	def __init__(self):
		self.oldself = dir(self)
		self.oldself.append("oldself")
	
	def __str__(self):
		childs = []
		
		for i in filter(lambda x: x not in self.oldself, dir(self)):
			childs.append(d.HTMLElement('<' + i + '>', [d.HTMLElement(eval("self." + str(i)))]))
		
		return d.HTMLElement("", [ d.HTMLElement("<book>", childs) ]).prettify()