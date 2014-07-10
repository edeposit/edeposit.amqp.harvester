#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# grada.cz checker v1.0.0 (28.03.2012) by Bystroushaak (bystrousak@kitakitsune.org)
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

data = unicode(ch.getPage("http://www.grada.cz/rss/rss.xml"), "windows-1250").encode("utf-8")


#= Main program ================================================================
for book in d.parseString(data).find("item"):
	if len(book.find("title")) == 0:
		continue
	
	b = Book()
	b.name = book.find("title")[0].getContent().strip()
	b.url = book.find("link")[0].getContent().strip()
	
	data = unicode(ch.getPage(b.url), "windows-1250").encode("utf-8")
	
	b.author = filter(lambda x: "Autor:" in x, data.splitlines())
	if len(b.author) > 0:
		b.author = ch.getVisibleText(b.author[0]).replace("Autor:", "")
	
	dom     = d.parseString(data)
	b.cost  = ch.getVisibleText(dom.find("div", {"class":"prices"})[0].getContent()).replace("Cena:", "").replace("Kč", "").strip()
	b.descr = ch.getVisibleText(dom.find("div", {"class":"content"})[0].getContent())
	
	print b
