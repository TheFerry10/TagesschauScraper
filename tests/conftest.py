import pytest
from bs4 import BeautifulSoup

from tagesschauscraper import article, teaser
from tagesschauscraper.constants import (
    ARTICLE_TEST_DATA_DIR,
    TEASER_TEST_DATA_DIR,
)
from tests.unit.test_archive import ARCHIVE_TEST_DATA_DIR


@pytest.fixture
def archive_valid_header():
    file_name = "valid_header.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture
def archive_invalid_header():
    file_name = "invalid_header.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture
def archive_news_categories():
    file_name = "news_categories.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture
def archive_date():
    file_name = "date.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture
def archive_teaser_container():
    file_name = "teaser_container.html"
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="archive_html")
def archive_html_(request):
    file_name = request.param
    with open(
        ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="article_html")
def teaser_html_(request):
    file_name = request.param
    with open(
        ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="valid_article")
def valid_article_():
    file_name = "valid-article.html"
    with open(
        ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return article.ArticleScraper(soup)


@pytest.fixture(name="valid_teaser")
def valid_teaser_():
    file_name = "valid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return teaser.TeaserScraper(soup)
