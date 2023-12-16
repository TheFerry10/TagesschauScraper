from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import pytest
import requests
from bs4 import BeautifulSoup

from tagesschauscraper.archive import (
    Archive,
    ArchiveFilter,
    create_request_params,
    get_archive_response,
)
from tagesschauscraper.article import Article, get_article_response
from tagesschauscraper.constants import ARCHIVE_URL, TAGESSCHAU_URL
from tagesschauscraper.teaser import Teaser

ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")
ARTICLE_TEST_DATA_DIR = Path("tests/data/article/")
TEASER_TEST_DATA_DIR = Path("tests/data/teaser/")

# test if Archive URL and request params are valid
# test integration between archive and teaser extraction
# test integration between teaser list and article


@pytest.fixture(name="request_params")
def request_params_():
    date_ = date(2023, 11, 4)
    category = "wirtschaft"
    archive_filter = ArchiveFilter(date_, category)
    return create_request_params(archive_filter)


@pytest.fixture(name="expected_archive_html")
def archive_html():
    file_name = "valid_header.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture(name="expected_article_html")
def article_html():
    file_name = "valid-article.html"
    with open(ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture(name="archive_with_teaser_list_html")
def article_teaser_html():
    file_name = "valid-teaser.html"
    with open(TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


def test_integration_between_archive_and_teaser_extraction(
    archive_with_teaser_list_html,
):
    expected_teaser_list = [
        {
            "date": "08.10.2023 • 13:17 Uhr",
            "topline": "Hamas-Großangriff auf Israel",
            "headline": "Weiter Kämpfe an mehreren Orten",
            "shorttext": "\n                    Nach den massiven Angriffen der Hamas gehen die Gefechte auf\n                    israelischem Boden weiter. Die Zahl der Toten steigt auf beiden\n                    Seiten: Insgesamt wurden mehr als 600 Opfer gemeldet. Laut Israel hält\n                    die Hamas weiterhin Geiseln fest.\n                    mehr\n",
            "article_link": "/ausland/asien/gaza-israel-angriff-108.html",
        }
    ]
    soup = BeautifulSoup(archive_with_teaser_list_html, "html.parser")
    archive = Archive(soup)
    extracted_teaser_list = [
        Teaser(teaser).extract() for teaser in archive.extract_teaser_list()
    ]
    assert extracted_teaser_list == expected_teaser_list


@patch("tagesschauscraper.article.requests.get")
def test_integration_between_teaser_list_and_article(mock_get, expected_article_html):
    teaser_list = [
        {
            "date": "08.10.2023 • 13:17 Uhr",
            "topline": "Dummy topline...",
            "headline": "Dummy headline",
            "shorttext": "Dummy text",
            "article_link": "/dummy/article.html",
        }
    ]
    for teaser in teaser_list:
        link = teaser["article_link"]
        mock_get.return_value.ok = True
        mock_get.return_value.text = expected_article_html
        response = get_article_response(link)
        soup = BeautifulSoup(response.text, "html.parser")
        article = Article(soup)
        structured_article = article.extract()
        structured_article["article_link"] = teaser["article_link"]
        assert structured_article == {
            "tags": ["\nHackerangriff\n", "\nDarknet\n", "\nHotel\n"],
            "article_link": "/dummy/article.html",
        }


@patch("tagesschauscraper.archive.requests.get")
def test_archive_html_from_url(mock_get, request_params, expected_archive_html):
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_archive_html
    response = get_archive_response(request_params)
    assert response is not None
    assert response.text == expected_archive_html


@patch("tagesschauscraper.article.requests.get")
def test_article_html_from_url(mock_get, expected_article_html):
    link = "/article.html"
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_article_html
    response = get_article_response(link)
    assert response is not None
    assert response.text == expected_article_html
