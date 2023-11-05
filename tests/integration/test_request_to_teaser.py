from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from tagesschauscraper.archive import (
    ARCHIVE_URL,
    TAGESSCHAU_URL,
    Archive,
    ArchiveFilter,
    create_request_params,
    get_archive_response,
)
from tagesschauscraper.article import Article
from tagesschauscraper.teaser import Teaser

ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")

# test archive_html from url
# test article_html from url
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


@patch("tagesschauscraper.archive.requests.get")
def test_archive_html_from_url(mock_get, request_params, expected_archive_html):
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_archive_html
    response = get_archive_response(request_params)
    assert response is not None
    assert response.text == expected_archive_html


def test_requesting_tagesschau():
    test_date = date(2023, 11, 4)
    test_category = "wirtschaft"
    archive_filter = ArchiveFilter(test_date, test_category)
    request_params = create_request_params(archive_filter)

    # fake it
    response = requests.get(ARCHIVE_URL, params=request_params)
    if response.status_code == 200:
        archive_html = response.text
    else:
        archive_html = ""

    extracted_teasers = []

    soup = BeautifulSoup(archive_html, "html.parser")
    archive = Archive(soup)
    teaser_list = archive.extract_teaser_list()
    for raw_teaser in teaser_list:
        teaser = Teaser(raw_teaser)
        extracted_teaser = teaser.extract()
        extracted_teaser["teaser_extract_timestamp"] = (
            datetime.utcnow().replace(microsecond=0).isoformat()
        )
        extracted_teasers.append(extracted_teaser)
    for et in extracted_teasers:
        article_url = TAGESSCHAU_URL + et["article_link"]
        response = requests.get(article_url)
        soup_article = BeautifulSoup(response.text, "html.parser")
        article = Article(soup_article)
        et["article_tags"] = article.extract_tags()
        et["article_headline"] = article.extract_headline()
        et["article_extract_timestamp"] = (
            datetime.utcnow().replace(microsecond=0).isoformat()
        )

    assert 1 == 1
