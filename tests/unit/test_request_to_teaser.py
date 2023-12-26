import datetime
from typing import List
from unittest.mock import patch

from bs4 import BeautifulSoup

from tagesschauscraper.domain.archive import Archive, get_archive_response
from tagesschauscraper.domain.article import (
    Article,
    ArticleScraper,
    get_article_response,
)
from tagesschauscraper.domain.teaser import Teaser, TeaserScraper


def test_integration_between_archive_and_teaser_extraction(
    archive_with_teaser_list_html,
):
    expected_teaser = Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
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
def test_integration_between_teaser_list_and_article(mock_get, expected_article_html):
    expected_article_list = [
        Article(
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
    ]
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
    article_list: List[Article] = []
    for t in teaser_list:
        mock_get.return_value.ok = True
        mock_get.return_value.text = expected_article_html
        response = get_article_response(t.article_link)
        soup = BeautifulSoup(response.text, "html.parser")
        article = ArticleScraper(soup).extract(
            extraction_timestamp=datetime.datetime(2023, 1, 1)
        )
        article.article_link = t.article_link
        article_list.append(article)
        assert article_list == expected_article_list


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
