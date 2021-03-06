#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser as d

from harvester.scrappers import ben_cz


# Functions & objects =========================================================
class MockDownloader(object):
    def __init__(self, test_data):
        self.test_data = test_data

    def download(self, url):
        return self.test_data


def test_get_last_td():
    test_str = """
    <td>first</td>
    <td>second</td>
    <td>last</td>
    """
    result = ben_cz._get_last_td(
        d.parseString(test_str)
    )

    assert result
    assert result.getContent() == "last"


def test_get_last_td_tag_not_found():
    # test behavior when tag is not found
    test_str = """
    <tr>first</tr>
    <tr>second</tr>
    <tr>last</tr>
    """
    result = ben_cz._get_last_td(
        d.parseString(test_str)
    )

    assert not result
    assert result is None


def test_get_td_or_none():
    test_str = """
    <tr>
        <td>xe</td>
    </tr>
    <tr id="random_id">
        <td>xe</td>
    </tr>
    <tr id="some_id">
        <td>first</td>
        <td>second</td>
        <td>last</td>
    </tr>
    <tr id="random_id>
        <td>xe</td>
    </tr>
    """
    result = ben_cz._get_td_or_none(
        d.parseString(test_str),
        "some_id"
    )

    assert result == "last"


def test_get_td_or_none_tag_not_found():
    # test behavior when tag is not found
    test_str = """
    <tr>
        <td>xe</td>
    </tr>
    <tr id="random_id">
        <td>xe</td>
    </tr>
    <tr id="random_id>
        <td>xe</td>
    </tr>
    """
    result = ben_cz._get_td_or_none(
        d.parseString(test_str),
        "some_id"
    )

    assert not result
    assert result is None


def test_parse_title():
    html = """
    <head>
        <title>Ignored title</title>
    </head>
    <body>
        <h1>Title</h1>
        <h1>Another title</h1>
    </body>
    """

    dom = d.parseString(html)
    result = ben_cz._parse_title(
        dom,
        dom.find("body")[0]
    )

    assert result
    assert result == "Title"


def test_parse_title_h1_not_found():
    # when the <h1> is not found
    html = """
    <head>
        <title>Ignored title</title>
    </head>
    <body>
        <h2>Title</h2>
        <h2>Another title</h2>
    </body>
    """

    dom = d.parseString(html)
    result = ben_cz._parse_title(
        dom,
        dom.find("body")[0]
    )

    assert result
    assert result == "Ignored title"


def test_parse_title_not_found():
    # if no title is found, raise exception
    html = """
    <head>
    </head>
    <body>
    </body>
    """

    dom = d.parseString(html)
    with pytest.raises(AssertionError):
        result = ben_cz._parse_title(
            dom,
            dom.find("body")[0]
        )


def test_parse_authors_multiple():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowAutor">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell2">autor</th>
        <td id="ctl00_ContentPlaceHolder1_TableCell2">
            <a href="first_url" title="Všechny knihy od First Author">First Author</a>,
            <a href="second_url" title="Všechny knihy od Second Author">Second Author</a>
        </td>
    </tr>
    """

    result = ben_cz._parse_authors(d.parseString(html))

    assert result
    assert len(result) == 2
    assert result[0].name == "First Author"
    assert result[0].URL == "first_url"
    assert result[1].name == "Second Author"
    assert result[1].URL == "second_url"


def test_parse_authors_one():
    # only one author
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowAutor">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell2">autor</th>
        <td id="ctl00_ContentPlaceHolder1_TableCell2">
            <a href="one_url" title="Všechny knihy od One Author">One Author</a>
        </td>
    </tr>
    """

    result = ben_cz._parse_authors(d.parseString(html))

    assert result
    assert len(result) == 1
    assert result[0].name == "One Author"
    assert result[0].URL == "one_url"


def test_parse_authors_no_author():
    # no author specified
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowAutor">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell2">autor</th>
        <td id="ctl00_ContentPlaceHolder1_TableCell2">
            No author specified!
        </td>
    </tr>
    """

    result = ben_cz._parse_authors(d.parseString(html))

    assert result == []
    assert len(result) == 0


def test_parse_authors_missing_block():
    # author block is missing
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowAutor">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell2">autor</th>
    </tr>
    """

    result = ben_cz._parse_authors(d.parseString(html))

    assert result == []
    assert len(result) == 0


def test_parse_authors_no_html():
    # no html found
    html = ""

    result = ben_cz._parse_authors(d.parseString(html))

    assert result == []
    assert len(result) == 0


def test_parse_publisher():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowNakladatel">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell3">vydal / výrobce</th>
        <td id="ctl00_ContentPlaceHolder1_TableCell3">
            <a href="http://shop.ben.cz/Produkty.aspx?lang=cz&nak=BEN+-+technick%c3%a1+literatura" title="Všechny knihy nakladatelství BEN - technická literatura">BEN - technická literatura</a>
        </td>
    </tr>
    """

    result = ben_cz._parse_publisher(d.parseString(html))

    assert result
    assert result == "BEN - technická literatura"


def test_parse_publisher_is_blank():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowNakladatel">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell3">vydal / výrobce</th>
        <td id="ctl00_ContentPlaceHolder1_TableCell3">
        </td>
    </tr>
    """

    result = ben_cz._parse_publisher(d.parseString(html))

    assert result is None


def test_parse_publisher_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowNakladatel">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell3">vydal / výrobce</th>
    </tr>
    """

    result = ben_cz._parse_publisher(d.parseString(html))

    assert result is None


def test_parse_publisher_no_html():
    html = ""

    result = ben_cz._parse_publisher(d.parseString(html))

    assert result is None


def test_parse_price():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowBeznaCena">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell10">
            <span title="Cena, za kterou se zboží prodává v kamenných obchodech.">
                běžná cena
            </span>
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell10">100,00 Kč</td>
    </tr>
    """

    result = ben_cz._parse_price(d.parseString(html))

    assert result
    assert result == "100,00 Kč"


def test_parse_price_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowBeznaCena">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell10">
            <span title="Cena, za kterou se zboží prodává v kamenných obchodech.">
                běžná cena
            </span>
        </th>
    </tr>
    """

    result = ben_cz._parse_price(d.parseString(html))

    assert result is None


def test_parse_price_no_html():
    html = ""

    result = ben_cz._parse_price(d.parseString(html))

    assert result is None


def test_parse_pages_binding():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">
            rozsah / vazba
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell4">1 strana / pevná</td>
    </tr>
    """

    pages, binding = ben_cz._parse_pages_binding(d.parseString(html))

    assert pages
    assert binding

    assert pages == "1 strana"
    assert binding == "pevná"


def test_parse_pages_binding_binding_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">
            rozsah / vazba
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell4">1 strana</td>
    </tr>
    """

    pages, binding = ben_cz._parse_pages_binding(d.parseString(html))

    assert pages
    assert not binding

    assert pages == "1 strana"
    assert binding is None


def test_parse_pages_binding_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">
            rozsah / vazba
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell4"></td>
    </tr>
    """

    pages, binding = ben_cz._parse_pages_binding(d.parseString(html))

    assert not pages
    assert not binding

    assert pages is None
    assert binding is None


def test_parse_pages_binding_tag_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">
            rozsah / vazba
        </th>
    </tr>
    """

    pages, binding = ben_cz._parse_pages_binding(d.parseString(html))

    assert not pages
    assert not binding

    assert pages is None
    assert binding is None


def test_parse_pages_binding_tag_no_html():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">
            rozsah / vazba
        </th>
    </tr>
    """

    pages, binding = ben_cz._parse_pages_binding(d.parseString(html))

    assert not pages
    assert not binding

    assert pages is None
    assert binding is None


def test_parse_ISBN_EAN():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowIsbnEan">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell7">
            ISBN / EAN
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell7">
            978-80-7310-514-6 / 9788073105146
        </td>
    </tr>
    """

    isbn, ean = ben_cz._parse_ISBN_EAN(d.parseString(html))

    assert isbn
    assert ean

    assert isbn == "978-80-7310-514-6"
    assert ean == "9788073105146"


def test_parse_ISBN_EAN_no_ean():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowIsbnEan">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell7">
            ISBN / EAN
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell7">
            978-80-7310-514-6
        </td>
    </tr>
    """

    isbn, ean = ben_cz._parse_ISBN_EAN(d.parseString(html))

    assert isbn
    assert not ean

    assert isbn == "978-80-7310-514-6"
    assert ean is None


def test_parse_ISBN_EAN_not_found():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowIsbnEan">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell7">
            ISBN / EAN
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell7"></td>
    </tr>
    """

    isbn, ean = ben_cz._parse_ISBN_EAN(d.parseString(html))

    assert not isbn
    assert not ean

    assert isbn is None
    assert ean is None


def test_parse_ISBN_EAN_no_tag():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowIsbnEan">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell7">
            ISBN / EAN
        </th>
    </tr>
    """

    isbn, ean = ben_cz._parse_ISBN_EAN(d.parseString(html))

    assert not isbn
    assert not ean

    assert isbn is None
    assert ean is None


def test_parse_ISBN_EAN_no_html():
    html = ""

    isbn, ean = ben_cz._parse_ISBN_EAN(d.parseString(html))

    assert not isbn
    assert not ean

    assert isbn is None
    assert ean is None


def test_parse_edition():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowVydani">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell5">
            vydání
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell5">1. české</td>
    </tr>
    """

    result = ben_cz._parse_edition(d.parseString(html))

    assert result
    assert result == "1. české"


def test_parse_edition_missing():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowVydani">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell5">
            vydání
        </th>
        <td id="ctl00_ContentPlaceHolder1_TableCell5"></td>
    </tr>
    """

    result = ben_cz._parse_edition(d.parseString(html))

    assert result is None


def test_parse_edition_no_tag():
    html = """
    <tr id="ctl00_ContentPlaceHolder1_tblRowVydani">
        <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell5">
            vydání
        </th>
    </tr>
    """

    result = ben_cz._parse_edition(d.parseString(html))

    assert result is None


def test_parse_edition_no_html():
    html = ""

    result = ben_cz._parse_edition(d.parseString(html))

    assert result is None


def test_parse_description():
    html = """
    <div class="detailKat">This shouldn't be here.</div>
    <h3>Popis</h3>
    <div class="detailPopis">
        Some <without tags=True />description.
        <p class="detailKat">This shouldn't be here.</p>
    </div>
    """

    result = ben_cz._parse_description(d.parseString(html))

    assert result
    assert result == "Some description."


def test_parse_description_no_other_tags():
    html = """
    <div class="detailPopis">
        Some <without tags=True />description.
    </div>
    """

    result = ben_cz._parse_description(d.parseString(html))

    assert result
    assert result == "Some description."


def test_parse_description_missing():
    html = """
    <div class="detailPopis"></div>
    """

    result = ben_cz._parse_description(d.parseString(html))

    assert result is None


def test_parse_description_no_tag():
    html = """
    xe
    <div>something</div>
    something else
    """

    result = ben_cz._parse_description(d.parseString(html))

    assert result is None


def test_parse_description_no_html():
    html = ""

    result = ben_cz._parse_description(d.parseString(html))

    assert result is None


def test_process_book():
    test_data = """<div id="contentDetail">
   <h1 class="line-remove">
      Title of the book.
   </h1>
   <div id="ctl00_ContentPlaceHolder1_panelDetail">
      <h2 class="line-add">
         Some random message.
      </h2>
      <div id="knihaDetail">
         <span class="detailImg">
            <span class="ruzek sleva"></span><img src="/images/obrazekneni.png" alt="First Author, Second Author, Third Author, Fourth Author:  Title of the book." title="First Author, Second Author, Third Author, Fourth Author:  Title of the book." /></span>
         <table border="0" id="ctl00_ContentPlaceHolder1_tblDetail">
        <tr id="ctl00_ContentPlaceHolder1_tblRowObjednaciCislo">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell1">obj. číslo</th><td id="ctl00_ContentPlaceHolder1_TableCell1">Don't care about this</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowAutor">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell2">autor</th><td id="ctl00_ContentPlaceHolder1_TableCell2"><a href="first_url" title="Všechny knihy od First Author">First Author</a>, <a href="second_url" title="Všechny knihy od Second Author">Second Author</a>, <a href="third_url" title="Všechny knihy od Third Author">Third Author</a>, <a href="fourth_url" title="Všechny knihy od Fourth Author">Fourth Author</a></td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowNakladatel">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell3">vydal / výrobce</th><td id="ctl00_ContentPlaceHolder1_TableCell3"><a href="http://shop.ben.cz/Produkty.aspx?lang=cz&nak=BEN+-+technick%c3%a1+literatura" title="Všechny knihy nakladatelství BEN - technická literatura">BEN - technická literatura</a></td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowRozsahVazba">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell4">rozsah / vazba</th><td id="ctl00_ContentPlaceHolder1_TableCell4">1 strana / pevná</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowVydani">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell5">vydání</th><td id="ctl00_ContentPlaceHolder1_TableCell5">1. české</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowDatumVydani">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell6">prodáváme od</th><td id="ctl00_ContentPlaceHolder1_TableCell6">2014</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowIsbnEan">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell7">ISBN / EAN</th><td id="ctl00_ContentPlaceHolder1_TableCell7">978-80-7310-514-6 / 9788073105146</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowDostupnost">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell8">dostupnost</th><td id="ctl00_ContentPlaceHolder1_TableCell8">Obvykle skladem</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowDostupnostHLink">
            <th id="ctl00_ContentPlaceHolder1_TableHeaderCell81">&nbsp;</th><td id="ctl00_ContentPlaceHolder1_TableCell81"><a href="http://praha.ben.cz:8235/114566.htm" onclick="javascript:skladem('http://praha.ben.cz:8235/114566.htm');return(false)" onkeypress="javascript:skladem('http://praha.ben.cz:.htm');return(false)">Ověřit dostupnost</a>&nbsp;&nbsp;<img src="http://shop.ben.cz/images/ik-new-win.jpg" style="border:none" border="0" /></td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowBeznaCena">
            <th scope="row" id="ctl00_ContentPlaceHolder1_TableHeaderCell10">
                  <span title="Cena, za kterou se zboží prodává v kamenných obchodech.">běžná cena</span>
               </th><td id="ctl00_ContentPlaceHolder1_TableCell10">100,00 Kč</td>
        </tr><tr id="ctl00_ContentPlaceHolder1_tblRowVaseCena">
            <th scope="row" style="height:19px;" id="ctl00_ContentPlaceHolder1_TableHeaderCell11">
                  <strong title="Zvýhodněná internetová cena pro přihlášené zákazníky.">
                     vaše cena</strong>
               </th><td style="height:19px;" id="ctl00_ContentPlaceHolder1_TableCell11" class="priceHighlight">
                  <strong>
                     100,00 Kč</strong>
                  (včetně 15% DPH)</td>
        </tr>
    </table>
         <div id="ctl00_ContentPlaceHolder1_panelObjednat">
            <div>
               <label for="pocetks">
                  Objednat
               </label>
               
               <input name="ctl00$ContentPlaceHolder1$txtPocetKs" value="1" maxlength="4" type="text" id="ctl00_ContentPlaceHolder1_txtPocetKs" size="4" />
               ks
               <input src="../images/btn-cart.png" style="border-width:0px;" name="ctl00$ContentPlaceHolder1$btnObjednat" id="ctl00_ContentPlaceHolder1_btnObjednat" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;ctl00$ContentPlaceHolder1$btnObjednat&quot;, &quot;&quot;, true, &quot;&quot;, &quot;&quot;, false, false))" type="image" class="btnKosik" />
               <a href="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;ctl00$ContentPlaceHolder1$lButtonObjednat&quot;, &quot;&quot;, true, &quot;&quot;, &quot;&quot;, false, true))" id="ctl00_ContentPlaceHolder1_lButtonObjednat">Koupit</a>
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
               <div style="color:Red;display:none;" id="ctl00_ContentPlaceHolder1_validSummary">
        </div>
            </div>
    </div>
         <p class="aktualizovano">
            Don't care about this.
         </p>
         <div class="detailKat">This shouldn't be here.</div>
         <h3>
            Popis</h3>
         <div class="detailPopis">
            Some <without tags=True />description.
            <p class="detailKat">This shouldn't be here.</p>
         </div>
      </div>
</div>
</div>

"""
    mock_downer = MockDownloader(test_data)
    ben_cz.DOWNER = mock_downer

    pub = ben_cz._process_book("some_url")

    assert pub.title == "Title of the book."
    assert pub.price == "100,00 Kč"
    assert pub.publisher == "BEN - technická literatura"

    assert len(pub.authors) == 4
    assert pub.authors[0].name == "First Author"
    assert pub.authors[0].URL == "first_url"
    assert pub.authors[1].name == "Second Author"
    assert pub.authors[1].URL == "second_url"
    assert pub.authors[2].name == "Third Author"
    assert pub.authors[2].URL == "third_url"
    assert pub.authors[3].name == "Fourth Author"
    assert pub.authors[3].URL == "fourth_url"

    assert pub.optionals.pages == "1 strana"
    assert pub.optionals.ISBN == "978-80-7310-514-6"
    assert pub.optionals.EAN == "9788073105146"
    assert pub.optionals.URL == "some_url"
    assert pub.optionals.binding == "pevná"
    assert pub.optionals.edition == "1. české"
    assert pub.optionals.description == "Some description."
