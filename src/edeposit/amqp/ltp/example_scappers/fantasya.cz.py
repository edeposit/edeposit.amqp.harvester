#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Fantasya.cz checker v1.0.0 (05.05.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 
# Unported License (http://creativecommons.org/licenses/by-nc-sa/3.0/cz/).
# Created in §Editor text editor.
#
#   Pokud hodlate pouzivat tento script, byl bych rad za zpetnou vazbu v podobe kratkeho informacniho 
#   emailu (napriklad maly popis kde budete script vyuzivat, nebo jen zminku o tom ze script pouzivate).
#   U vetsiny scriptu co jsem stvoril totiz nemam tuseni jestli upadly do zapomeni, nebo jsou uzitecne 
#   i nekomu jinemu nez me. Diky.
#
#   If you want to use this script, I'd be happy if you drop me a small feedback message. For example 
#   something about where you use this script, or just a message that this script is useful for you.
#   For most of my scripts, I dont know if they are forgotten, or they are usefull for other people.
#   Thanks.
#   
#
# Notes:
    # 
#===============================================================================
# Imports ======================================================================
#===============================================================================
import os
import os.path
import sys
import time
import shelve


import CheckerTools as c
import dhtmlparser as d


# react to queries
if len(sys.argv) > 1:
	if sys.argv[1] == "--next-run":
		print int(time.time()) + (60 * 60 * 24 * 7) # once per wekS
	elif sys.argv[1] == "--timeout":
		print 60 * 5 # 5m
	
	sys.exit(0)



#===============================================================================
# Variables ====================================================================
#===============================================================================
SEARCHES_TXT = "searches.txt"

base_url = "http://www.fantasya.cz"
url = base_url + "/shop_browse.php?where=shop_product&referrer=search&keywords="
db = shelve.open("old_books.dat")

if db.has_key("old"):
	old = db["old"]
else:
	old = {}

if os.path.exists(SEARCHES_TXT):
	file = open(SEARCHES_TXT)
	searches = map(lambda x: x.strip().replace(" ", "+"), file.read().splitlines())
else:
	sys.stderr.write("Searches not defined!\nCreate file '" + SEARCHES_TXT + "' and fill it with something, god dammit!\n")
	sys.exit(0)


#===============================================================================
#= Main program ================================================================
#===============================================================================
mail = "Fantasya checker brings you new content:\n\n"

send = False
for keyword in searches:
	data = c.getPage(url + keyword)

	if keyword not in old:
		old[keyword] = []
	
	for l in d.parseString(data).find("a"):
		if "href" in l.params and l.params["href"].startswith("/zbozi/") and len(l.childs) > 0 and not l.childs[0].isTag():
			name = l.getContent()
			link = base_url + l.params["href"]
		
			if name not in old[keyword]:
				if keyword not in mail:
					mail += "\nKeyword: " + keyword + ";"
				mail += "\t" + name + "; " + link + "\n"
			
				send = True
				old[keyword].append(name)


# payload
if send:
	if 0 != os.system("mailer -f hlubina@internetu.net -t bystrousak@kitakitsune.org -s 'Fantasya.cz checker' <<LKNDFOJASDKJ-\n" + mail + "\nLKNDFOJASDKJ-"):
		raise Exception("Can't send mail! Check your mailer!")


db["old"] = old
db.close()
