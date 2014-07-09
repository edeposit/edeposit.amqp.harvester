#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# zonerpress.cz v1.0.0 (28.03.2012) by Bystroushaak (bystrousak@kitakitsune.org)
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
for book in d.parseString(ch.getPage("http://zonerpress.cz/inshop/scripts/rss.aspx")).find("item"):
	if len(book.find("title")) == 0:
		continue
	
	b = Book()
	b.name = book.find("title")[0].getContent().strip()
	b.url = book.find("link")[0].getContent()
	
	dom = d.parseString(ch.getPage(b.url))
	
	b.descr = ch.getVisibleText(dom.find("div", {"class":"popis"})[0].getContent())
	b.cost  = ch.getVisibleText(dom.find("p", {"class":"cenatext"})[0].getContent()).replace("&nbsp;", " ")
	
	for i in dom.find("table", {"class":"tabulka-info"})[0].find("tr"):
		if "Autor" in i.getContent():
			b.author = ch.getVisibleText(i.getContent()).replace("\n", "").replace("Autor:", "")
			break
	
	print b