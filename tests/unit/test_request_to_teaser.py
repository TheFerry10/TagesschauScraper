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


@patch("tagesschauscraper.domain.archive.requests.get")
def test_archive_html_from_url(
    mock_get, request_params, expected_archive_html
):
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_archive_html
    response = get_archive_response(request_params)
    assert response is not None
    assert response.text == expected_archive_html


@patch("tagesschauscraper.domain.article.requests.get")
def test_article_html_from_url(mock_get, expected_article_html):
    link = "/article.html"
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_article_html
    response = get_article_response(link)
    assert response is not None
    assert response.text == expected_article_html
