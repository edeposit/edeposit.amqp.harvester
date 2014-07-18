#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

by Bystroushaak (bystrousak@kitakitsune.org
"""
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 Unported License
# (http://creativecommons.org/licenses/by/3.0/).
#
#= Imports ====================================================================
from httpkie import Downloader
import dhtmlparser as d



#= Variables ==================================================================
URL = "http://shop.ben.cz/cz/kategorie/novinky/knihy-za-posledni-tri-mesice-pouze-ben-technicka-literatura.aspx"



#= Functions & objects ========================================================
def getBooks():
    downer = Downloader()
    data = downer.download(URL)

    dom = d.parseString(data)

    books = []
    for html_chunk in dom.find("div", {"class": "seznamKniha"}):
        book = {}

        # name is separated by ":" from author
        name = html_chunk.find("a")[0].params["title"]
        if ":" in name:
            book["author"] = name.split(":")[0].strip()
            book["name"]   = "".join(name.split(":")[1:]).strip()
        else:
            book["name"] = name

        book["url"]   = html_chunk.find("a")[0].params["href"]
        book["cost"]  = html_chunk.find("p", {"class": "seznamCena"})[0]\
                                  .find("strong")[0].getContent().split("Kč")[0]\
                                  .strip()

        descr = downer.download(html_chunk.find("a")[0].params["href"])
        descr = d.parseString(descr.decode("utf-8").encode("utf-8"))  # it works :D
        descr = descr.find("div", {"class": "detailPopis"})[0]
        descr = str(descr).split("<ol>")[0]
        descr = descr.split("</table>")[1] if "</table>" in descr else descr
        book["descr"] = d.removeTags(descr).strip()

        books.append(book)

    return books


#= Main program ===============================================================
if __name__ == '__main__':
    print getBooks()[0]["descr"]

# TODO:
# serializace do jsonu jen při spuštění
# unittest nějak.. (sekce seznamKniha by tam měla být vždy, ne?)