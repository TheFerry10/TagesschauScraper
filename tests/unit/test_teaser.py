import datetime
from unittest.mock import patch
import pytest
from bs4 import BeautifulSoup

from tagesschauscraper.domain import teaser
from tagesschauscraper.domain.constants import TEASER_TEST_DATA_DIR
from tagesschauscraper.domain.teaser import Teaser


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
    return teaser.TeaserScraper(soup)


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
    teaser_ = teaser.TeaserScraper(soup)
    assert teaser_.valid is is_valid


@pytest.mark.parametrize(
    "teaser_html,expected_link_to_article",
    [
        pytest.param(
            "valid-teaser.html",
            "/dummy/article.html",
            id="valid",
        ),
        pytest.param("invalid-teaser.html", None, id="invalid"),
    ],
    indirect=["teaser_html"],
)
def test_extract_link_to_article(teaser_html, expected_link_to_article):
    soup = BeautifulSoup(teaser_html, "html.parser")
    teaser_ = teaser.TeaserScraper(soup)
    link_to_article = teaser_.extract_article_link()
    assert expected_link_to_article == link_to_article


def test_extract_topline(valid_teaser):
    expected_topline = "Test topline"
    topline = valid_teaser.extract_topline()
    assert topline == expected_topline


def test_extract_headline(valid_teaser):
    expected_headline = "Test headline"
    headline = valid_teaser.extract_headline()
    assert headline == expected_headline


def test_extract_shorttext(valid_teaser):
    expected_shorttext = "Test short text"
    shorttext = valid_teaser.extract_shorttext()
    assert shorttext == expected_shorttext


def test_extract_date(valid_teaser):
    expected_date = "08.10.2023 • 13:17 Uhr"
    topline = valid_teaser.extract_date()
    assert topline == expected_date


@patch("tagesschauscraper.domain.teaser.get_extraction_timestamp")
def test_extract(mock_extraction_timestamp, valid_teaser):
    mock_extraction_timestamp.return_value = "2023-01-01T00:00:00"
    expectedTeaser = Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    teaser_ = valid_teaser.extract()
    assert teaser_ == expectedTeaser
