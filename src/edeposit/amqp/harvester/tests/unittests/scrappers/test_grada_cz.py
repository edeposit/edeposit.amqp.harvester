#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from harvester.scrappers import grada_cz as grada

from test_ben_cz import MockDownloader


# Variables ===================================================================
AUTHORS = """
<h3><a href="../dalsi-knihy-autora/Putsalek_Monika/" class="h2" title="Další knihy autora: Putšálek Monika">Putšálek Monika</a>, <a href="../dalsi-knihy-autora/Zich_Franta/" class="h2" title="Další knihy autora: Zich Franta"> Zich Franta</a></h3><br />
"""

AUTHOR = """
<h3><a href="../dalsi-knihy-autora/Putsalek_Monika/" class="h2" title="Další knihy autora: Putšálek Monika">Putšálek Monika</a></h3><br />
"""

HTML = """
<div class="item">
<div class="clearfix row-one">
<div class="picture"><a href="../url_to_the_catalog-6656489/kniha/katalog/" title=""><img src="../images_knihy/784848410.jpg" height="123" width="88" alt="" class="border" /></a> <div class="prices"> Cena:
<b class="red">199</b> Kč </div>
</div>
<div class="comment">
<h2><a href="../url_to_the_catalog-6656489/kniha/katalog/" class="h1" title="Detail knihy: Main title">Main title</a><br /><span class="gray">Subtitle</span></h2>
$AUTHOR
<div class="perex">

Here should be long description.
</div>
<div class="price-overflow"> 
<br />17×24 cm | 153 stran | <b>978-80-249-5701-0</b> | Katalog. č. knihy: <b>65655</b> <br />
<!--[if !IE]> -->
<script src="http://connect.facebook.net/cs_CZ/all.js#xfbml=1" type="text/javascript"></script><fb:like show_faces="false" layout="button_count" send="true" width="450" href="http://www.facebook.com/grada.cz" font=""></fb:like>
<!-- <![endif]-->
</div>
</div>
</div>
<div class="row-one">
<div class="buttons clearfix">
<div class="f-r">
<form action="../basket/" method="post" class="objednat">
<div><input type="hidden" name="def_k" value="pall" /> <input
type="hidden" name="kat1" value="6575" /> <input
type="hidden" name="referer" value="/novinky/?start=0&krok=100" />
<input name="pocet1" value="1" type="text" class="form t-r" size="1" />
ks &nbsp; <input src="../images_buttons/objednat_off.gif" type="image" title="Objednat knihu: Alt Main title" />
</div>
</form>
</div>
<a href="../url_to_the_catalog-6656489/kniha/katalog/" title="Detail knihy: Alt Main title"><img src="../images_buttons/viceinformaci_off.gif" alt="Detail knihy: Alt Main title" height="22" /></a>&nbsp;<img src="../images_buttons/novinka.gif" alt="Novinka" height="22" /> </div>
</div>
</div>
"""
dom = dhtmlparser.parseString(HTML)


# Functions & objects =========================================================
def test_normalize_url():
    assert grada._normalize_url("../xex") == grada.BASE_URL + "/xex"
    assert grada._normalize_url("/xex") == grada.BASE_URL + "/xex"


def test_parse_alt_title():
    title = grada._parse_alt_title(dom)

    assert title == "Alt Main title"


def test_parse_title_url():
    dom = dhtmlparser.parseString(HTML)

    title, url = grada._parse_title_url(dom)

    assert title == "Main title"
    assert url == grada.BASE_URL + "/url_to_the_catalog-6656489/kniha/katalog/"

    # test alternative title lookup
    title = dom.find("div", {"class": "comment"})
    title[0].replaceWith(dhtmlparser.HTMLElement(""))

    title, url = grada._parse_title_url(dom)
    assert title == "Alt Main title"
    assert url is None


def test_parse_subtitle():
    dom = dhtmlparser.parseString(HTML)

    subtitle = grada._parse_subtitle(dom)
    assert subtitle == "Subtitle"

    # DOM without subtitle
    st = dom.find("span", {"class": "gray"})[0]
    st.replaceWith(dhtmlparser.HTMLElement())

    subtitle = grada._parse_subtitle(dom)
    assert subtitle is None


def test_parse_authors():
    pass


def test_parse_description():
    pass


def test_parse_format_pages_isbn():
    pass


def test_parse_price():
    pass


def test_process_book():
    pass
