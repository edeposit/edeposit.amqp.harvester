#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# cpress.cz checker v1.0.0 (28.03.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in Geany text editor.
#
# Notes:
    # 
#= Imports =====================================================================
import dhtmlparser as d
import CheckerTools as ch
from api.book import Book


#= Main program ================================================================
for url in ["http://knihy.cpress.cz/?p=news", "http://knihy.cpress.cz/?p=news&page=2", "http://knihy.cpress.cz/?p=news&page=3"]:
	for book in d.parseString(ch.getPage(url)).find("div", {"class":"polozka"}):
		b = Book()
		
		b.name   = book.find("h4")[0].childs[0].getContent()
		b.url    = book.find("h4")[0].childs[0].params["href"].strip()
		try:
			b.author = book.find("a", {"class":"autor"})[0].getContent()
		except IndexError:
			b.author = "Kolektiv"
		b.cost   = book.find("div", {"class":"cena"})[0].find("span")[0].getContent()
		
		try:
			b.descr = d.parseString(ch.getPage(b.url)).find("meta", {"name":"description"})[0].params["content"]
		except IndexError:
			try:
				b.descr = ch.getVisibleText(d.parseString(ch.getPage(b.url)).find("div", {"id":"zalozka1"})[0].getContent())
			except IndexError:
				b.descr = "none"
		
		print b