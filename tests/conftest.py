import datetime
import os
import shutil

import pytest
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from tagesschauscraper.adapters.orm import metadata, start_mappers
from tagesschauscraper.domain import helper
from tagesschauscraper.domain.archive import (
    ArchiveFilter,
    create_request_params,
)
from tagesschauscraper.domain.article import ArticleScraper
from tagesschauscraper.domain.constants import (
    ARCHIVE_TEST_DATA_DIR,
    ARTICLE_TEST_DATA_DIR,
    TEASER_TEST_DATA_DIR,
)
from tagesschauscraper.domain.teaser import TeaserScraper


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


@pytest.fixture
def sqlite_session():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    start_mappers()
    Session = sessionmaker(bind=engine)
    return Session()


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
    return ArticleScraper(soup)


@pytest.fixture(name="invalid_article")
def invalid_article_():
    file_name = "invalid-article.html"
    with open(
        ARTICLE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return ArticleScraper(soup)


@pytest.fixture(name="valid_teaser")
def valid_teaser_():
    file_name = "valid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    return soup


@pytest.fixture(name="archive_with_teaser_list_html")
def article_teaser_html():
    file_name = "valid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
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
