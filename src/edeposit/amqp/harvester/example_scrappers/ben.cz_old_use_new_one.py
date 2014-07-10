#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ben.cz checker v1.0.0 (28.03.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in Geany text editor.
#
# Notes:
    # 
#= Imports =====================================================================
import CheckerTools as ch
import dhtmlparser as d
from api.book import Book


#= Main program ================================================================
ben = ch.getPage("http://shop.ben.cz/cz/kategorie/novinky/knihy-za-posledni-tri-mesice-pouze-ben-technicka-literatura.aspx")

books = []
for book in d.parseString(ben).find("div", {"class":"seznamKniha"}):
	b = Book()
	
	# name is separated by ":" from author
	name = book.find("a")[0].params["title"]
	if ":" in name: 
		b.author = name.split(":")[0].strip()
		b.name   = "".join(name.split(":")[1:]).strip()
	else:
		b.name   = name
		b.author = ""
	
	b.url    = book.find("a")[0].params["href"]
	b.cost   = book.find("p", {"class": "seznamCena"})[0].find("strong")[0].getContent().split("Kč")[0].strip()
	b.descr  = ch.getVisibleText((d.parseString(ch.getPage(book.find("a")[0].params["href"])).find("div", {"class":"detailPopis"})[0].prettify().split("<ol>")[0]))
	
	print b






