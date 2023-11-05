from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper import teaser

TEASER_TEST_DATA_DIR = Path("tests/data/teaser/")


@pytest.fixture(name="teaser_html")
def teaser_html_(request):
    file_name = request.param
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="valid_teaser")
def valid_teaser_():
    file_name = "valid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return teaser.Teaser(soup)


@pytest.mark.parametrize(
    "teaser_html,is_valid",
    [
        pytest.param("valid-teaser.html", True, id="valid"),
        pytest.param("invalid-teaser.html", False, id="invalid"),
    ],
    indirect=["teaser_html"],
)
def test_teaser_with_input(teaser_html, is_valid):
    soup = BeautifulSoup(teaser_html, "html.parser")
    teaser_ = teaser.Teaser(soup)
    assert teaser_.valid is is_valid


@pytest.mark.parametrize(
    "teaser_html,expected_link_to_article",
    [
        pytest.param(
            "valid-teaser.html",
            "/ausland/asien/gaza-israel-angriff-108.html",
            id="valid",
        ),
        pytest.param("invalid-teaser.html", None, id="invalid"),
    ],
    indirect=["teaser_html"],
)
def test_extract_link_to_article(teaser_html, expected_link_to_article):
    soup = BeautifulSoup(teaser_html, "html.parser")
    teaser_ = teaser.Teaser(soup)
    link_to_article = teaser_.extract_article_link()
    assert expected_link_to_article == link_to_article


def test_extract_topline(valid_teaser):
    expected_topline = "Hamas-Großangriff auf Israel"
    topline = valid_teaser.extract_topline()
    assert topline == expected_topline


def test_extract_headline(valid_teaser):
    expected_headline = "Weiter Kämpfe an mehreren Orten"
    headline = valid_teaser.extract_headline()
    assert headline == expected_headline


def test_extract_shorttext(valid_teaser):
    expected_shorttext = """\n                    Nach den massiven Angriffen der Hamas gehen die Gefechte auf\n                    israelischem Boden weiter. Die Zahl der Toten steigt auf beiden\n                    Seiten: Insgesamt wurden mehr als 600 Opfer gemeldet. Laut Israel hält\n                    die Hamas weiterhin Geiseln fest.\n                    mehr\n"""
    shorttext = valid_teaser.extract_shorttext()
    assert shorttext == expected_shorttext


def test_extract_date(valid_teaser):
    expected_date = "08.10.2023 • 13:17 Uhr"
    topline = valid_teaser.extract_date()
    assert topline == expected_date


def test_extract(valid_teaser):
    expected_date = "08.10.2023 • 13:17 Uhr"
    expected_shorttext = """\n                    Nach den massiven Angriffen der Hamas gehen die Gefechte auf\n                    israelischem Boden weiter. Die Zahl der Toten steigt auf beiden\n                    Seiten: Insgesamt wurden mehr als 600 Opfer gemeldet. Laut Israel hält\n                    die Hamas weiterhin Geiseln fest.\n                    mehr\n"""
    expected_headline = "Weiter Kämpfe an mehreren Orten"
    expected_topline = "Hamas-Großangriff auf Israel"
    expected_article_link = "/ausland/asien/gaza-israel-angriff-108.html"
    expected_teaser_info = {
        "date": expected_date,
        "topline": expected_topline,
        "headline": expected_headline,
        "shorttext": expected_shorttext,
        "article_link": expected_article_link,
    }
    teaser_info = valid_teaser.extract()
    assert teaser_info == expected_teaser_info
