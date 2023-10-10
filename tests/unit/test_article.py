from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper import article

ARTICLE_TEST_DATA_DIR = Path("tests/data/article/")


@pytest.fixture(name="article_html")
def teaser_html_(request):
    file_name = request.param
    with open(ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture(name="valid_article")
def valid_article_():
    file_name = "valid-article.html"
    with open(ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return article.Article(soup)


@pytest.mark.parametrize(
    "article_html,is_valid",
    [
        pytest.param("valid-article.html", True, id="valid"),
        pytest.param("invalid-article.html", False, id="invalid"),
    ],
    indirect=["article_html"],
)
def test_can_classify_article_correctly(article_html, is_valid):
    soup = BeautifulSoup(article_html, "html.parser")
    article_ = article.Article(soup)
    assert article_.valid is is_valid


def test_extract_topline(valid_article: article.Article):
    expected_topline = 'Hacker-Angriff auf "Motel One"'
    topline = valid_article.extract_topline()
    assert topline == expected_topline


def test_extract_headline(valid_article: article.Article):
    expected_headline = "Daten von Hotelgästen im Darknet veröffentlicht"
    headline = valid_article.extract_headline()
    assert headline == expected_headline


def test_extract_metatextline(valid_article: article.Article):
    expected_metatextline = "Stand: 07.10.2023 17:43 Uhr"
    metatextline = valid_article.extract_metatextline()
    assert metatextline == expected_metatextline


def test_extract_subheads(valid_article: article.Article):
    expected_subheads = [
        "Offenbar-150-Kreditkartendaten-betroffen",
        "Notfalllisten-mit-Kundendaten-im-Darkweb",
    ]
    subheads = valid_article.extract_subheads()
    assert subheads == expected_subheads


def test_extract_paragraphs(valid_article: article.Article):
    expected_paragraphs = [
        (
            'Nach einem Hackerangriff auf die Hotelkette "Motel One" sind laut'
            " einem Medienbericht Millionen Namen und Reisedaten von Gästen"
            " online zu finden. Sechs Terabyte wurden laut dem Unternehmen"
            " gestohlen - darunter auch Kreditkartendaten."
        ),
        (
            'Bei der Hotelkette "Motel One" haben Hacker in großem Stil Daten'
            " mit privaten Informationen von Gästen geklaut und im Darknet"
            ' veröffentlicht. "Nach vorläufigen Erkenntnissen betreffen die'
            " gestohlenen Daten im Volumen von sechs Terabyte insbesondere"
            " Adress- und Rechnungsdaten von Kunden und nur sehr vereinzelt"
            ' Kreditkarteninformationen unserer Hotelgäste", sagte eine'
            " Sprecherin des Unternehmens auf Anfrage der Nachrichtenagentur"
            " dpa. "
        ),
    ]
    paragraphs = valid_article.extract_paragraphs()
    assert paragraphs == expected_paragraphs


def test_extract_tags(valid_article: article.Article):
    expected_tags = ["Hackerangriff", "Darknet", "Hotel"]
    tags = valid_article.extract_tags()
    assert tags == expected_tags
