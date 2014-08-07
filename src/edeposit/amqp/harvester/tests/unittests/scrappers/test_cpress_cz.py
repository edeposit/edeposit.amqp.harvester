#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from harvester.scrappers import cpress_cz


# Variables ===================================================================



# Functions & objects =========================================================
def test_parse_alt_title():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        </div>
        """
    )

    alt_title = cpress_cz._parse_alt_title(dom)

    assert alt_title == "Záhadná jízda králů"


def test_parse_alt_title_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        </div>
        """
    )

    with pytest.raises(UserWarning):
        cpress_cz._parse_alt_title(dom)


def test_parse_alt_title_param_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        </div>
        """
    )

    with pytest.raises(UserWarning):
        cpress_cz._parse_alt_title(dom)

def test_parse_alt_url():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    url = cpress_cz._parse_alt_url(dom)

    assert url
    assert url == cpress_cz.normalize_url(cpress_cz.BASE_URL, "zahadna-jizda-kralu/")


def test_parse_alt_url_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        </div>
        </div>
        """
    )

    url = cpress_cz._parse_alt_url(dom)

    assert url is None


def test_parse_title_url():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        <a href="zahadna-jizda-kralu/">Záhadná jízda králů</a>
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    title, url = cpress_cz._parse_title_url(dom)

    assert title == "Záhadná jízda králů"
    assert url == cpress_cz.normalize_url(cpress_cz.BASE_URL, "zahadna-jizda-kralu/")


def test_parse_title_url_tag_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    title, url = cpress_cz._parse_title_url(dom)

    assert title == "Záhadná jízda králů"
    assert url == cpress_cz.normalize_url(cpress_cz.BASE_URL, "zahadna-jizda-kralu/")


def test_parse_title_url_url_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail">Detail knihy</div>
        </div>
        </div>
        """
    )

    title, url = cpress_cz._parse_title_url(dom)

    assert title == "Záhadná jízda králů"
    assert url is None


def test_parse_authors():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        <a href="zahadna-jizda-kralu/">Záhadná jízda králů</a>
        </div>
        <div class="polozka_autor"><a href="autori/autor/jiri-jilik/">Jiří Jilík</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    authors = cpress_cz._parse_authors(dom)

    assert authors
    assert authors[0].name == "Jiří Jilík"
    assert authors[0].URL == cpress_cz.normalize_url(cpress_cz.BASE_URL, "autori/autor/jiri-jilik/")


def test_parse_authors_no_authors():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        <a href="zahadna-jizda-kralu/">Záhadná jízda králů</a>
        </div>
        <div class="polozka_autor"></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    authors = cpress_cz._parse_authors(dom)

    assert authors == []


def test_parse_authors_no_authors_tag():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        <a href="zahadna-jizda-kralu/">Záhadná jízda králů</a>
        </div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    authors = cpress_cz._parse_authors(dom)

    assert authors == []

def test_parse_authors_multiple_authors():
    dom = dhtmlparser.parseString(
        """
        <div class="polozka">
        <div class="polozka_obrazek">
        <a href="zahadna-jizda-kralu/">
        <img width="90" alt="Záhadná jízda králů" src="typo3temp/pics/8def5efbad.jpg" height="140" /> </a>
        </div>
        <div class="polozka_obsah">
        <div class="polozka_popisy">
        <div class="polozka_nazev">
        <a href="zahadna-jizda-kralu/">Záhadná jízda králů</a>
        </div>
        <div class="polozka_autor"><a href="autori/autor/leos-kopecky/">Leoš Kopecký</a>, <a href="autori/autor/roswitha-kammerl/">Roswitha Kammerl</a></div>
        <div class="polozka_podtitul">Nová kniha autora bestselleru Žítkovské čarování!</div>
        </div>
        <div class="polozka_cena">199&nbsp;Kč</div>
        <div class="polozka_detail"><a href="zahadna-jizda-kralu/">Detail knihy</a></div>
        </div>
        </div>
        """
    )

    authors = cpress_cz._parse_authors(dom)

    assert authors
    assert len(authors) == 2

    assert authors[0].name == "Leoš Kopecký"
    assert authors[0].URL == cpress_cz.normalize_url(cpress_cz.BASE_URL, "autori/autor/leos-kopecky/")
    assert authors[1].name == "Roswitha Kammerl"
    assert authors[1].URL == cpress_cz.normalize_url(cpress_cz.BASE_URL, "autori/autor/roswitha-kammerl/")


def test_parse_price():
    dom = dhtmlparser.parseString(
        """
        <div class="kniha_detail_cena">
        <ul>
        <li><label>((availability)):</label> <span>((availability_available))</span></li>
        <li><label>Doporučená cena:</label> <span class="cena">299 Kč</span></li>
        </ul>
        </div>
        """
    )

    price = cpress_cz._parse_price(dom)

    assert price == "299 Kč"


def test_parse_price_not_found():
    dom = dhtmlparser.parseString(
        """
        <div class="kniha_detail_cena">
        <ul>
        <li><label>((availability)):</label> <span>((availability_available))</span></li>
        </ul>
        </div>
        """
    )

    with pytest.raises(UserWarning):
        cpress_cz._parse_price(dom)


def test_parse_ean_date_format_():
    dom = dhtmlparser.parseString(
        """
            <table>
            <tr><th>Autor:</th> <td><a href="autori/autor/"> </a></td></tr>
            <tr><th>Žánr:</th> <td><a href="vydali-jsme/?tx_odbooks%5Bgenre%5D=93&cHash=718a579059d52191c53e0eb0125608c2">komiks</a></td></tr>
            <tr><th>Datum vydání:</th> <td>06. 08. 2014</td></tr>
            <tr><th>EAN:</th> <td>9788026404620</td></tr>
            </table>
            <table>
            <tr><th>Formát:</th> <td>210 x 297 mm brožovaná lepená</td></tr>
            </table>
            <br/>
        """
    )

    ean = cpress_cz._parse_ean(dom)
    date = cpress_cz._parse_date(dom)
    format = cpress_cz._parse_format(dom)

    assert ean == "9788026404620"
    assert date == "06. 08. 2014"
    assert format == "210 x 297 mm brožovaná lepená"


def test_parse_ean_date_format_not_found():
    dom = dhtmlparser.parseString(
        """
            <table>
            <tr><th>Autor:</th> <td><a href="autori/autor/"> </a></td></tr>
            <tr><th>Žánr:</th> <td><a href="vydali-jsme/?tx_odbooks%5Bgenre%5D=93&cHash=718a579059d52191c53e0eb0125608c2">komiks</a></td></tr>
            <tr><th>EAN:</th></tr>
            </table>
            <table>
            </table>
            <br/>
        """
    )

    ean = cpress_cz._parse_ean(dom)
    date = cpress_cz._parse_date(dom)
    format = cpress_cz._parse_format(dom)

    assert ean is None
    assert date is None
    assert format is None
