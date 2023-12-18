import datetime
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper.archive import (
    Archive,
    ArchiveFilter,
    create_request_params,
    get_archive_response,
)
from tagesschauscraper.article import (
    Article,
    ArticleScraper,
    get_article_response,
)
from tagesschauscraper.constants import (
    ARCHIVE_TEST_DATA_DIR,
    ARTICLE_TEST_DATA_DIR,
    TEASER_TEST_DATA_DIR,
)
from tagesschauscraper.teaser import Teaser, TeaserScraper


@pytest.fixture(name="request_params")
def request_params_():
    date_ = datetime.date(2023, 11, 4)
    category = "wirtschaft"
    archive_filter = ArchiveFilter(date_, category)
    return create_request_params(archive_filter)


@pytest.fixture(name="expected_archive_html")
def archive_html():
    file_name = "valid_header.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="expected_article_html")
def article_html():
    file_name = "valid-article.html"
    with open(
        ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="archive_with_teaser_list_html")
def article_teaser_html():
    file_name = "valid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


def test_integration_between_archive_and_teaser_extraction(
    archive_with_teaser_list_html,
):
    expected_date = "08.10.2023 • 13:17 Uhr"
    expected_shorttext = "Test short text"
    expected_headline = "Test headline"
    expected_topline = "Test topline"
    expected_article_link = "/ausland/test/tag1-tag2-108.html"
    expected_extraction_date = "2023-01-01T00:00:00"
    expected_teaser = Teaser(
        date=expected_date,
        shorttext=expected_shorttext,
        headline=expected_headline,
        topline=expected_topline,
        article_link=expected_article_link,
        extraction_timestamp=expected_extraction_date,
    )
    expected_teaser_list = [expected_teaser]
    soup = BeautifulSoup(archive_with_teaser_list_html, "html.parser")
    archive = Archive(soup)
    extracted_teaser_list = [
        TeaserScraper(t).extract(datetime.datetime(2023, 1, 1))
        for t in archive.extract_teaser_list()
    ]
    assert extracted_teaser_list == expected_teaser_list


@patch("tagesschauscraper.article.requests.get")
def test_integration_between_teaser_list_and_article(
    mock_get, expected_article_html
):
    expected_article = Article(
        abstract="Test abstract",
        topline="Test topline",
        headline="Test headline",
        metatextline="Stand: 07.10.2023 17:43 Uhr",
        paragraphs=["Paragraph 1"],
        subheads=["Subhead 1", "Subhead 2"],
        tags=["tag1", "tag2", "tag3"],
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    teaser_list = [
        Teaser(
            date="08.10.2023 • 13:17 Uhr",
            topline="Dummy topline...",
            headline="Dummy headline",
            shorttext="Dummy text",
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        )
    ]
    for t in teaser_list:
        mock_get.return_value.ok = True
        mock_get.return_value.text = expected_article_html
        response = get_article_response(t.article_link)
        soup = BeautifulSoup(response.text, "html.parser")
        article = ArticleScraper(soup).extract(
            extraction_timestamp=datetime.datetime(2023, 1, 1)
        )
        article.article_link = t.article_link
        assert article == expected_article


@patch("tagesschauscraper.archive.requests.get")
def test_archive_html_from_url(
    mock_get, request_params, expected_archive_html
):
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
