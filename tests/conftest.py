import datetime

import pytest
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from bluescraper.config import ConfigReader
from bluescraper.scraper import Scraper
from tagesschau.adapters.orm import metadata, start_mappers
from tagesschau.domain.constants import TEST_CONFIG_DIR, TEST_DATA_DIR
from tagesschau.domain.model import ArchiveFilter, create_request_params


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
def html(request):
    file_name = request.param
    with open(TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def soup(html):
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def config(request):
    config_file_name = request.param
    config_path = TEST_CONFIG_DIR.joinpath(config_file_name)
    config_reader = ConfigReader(config_path)
    return config_reader.load()


@pytest.fixture
def scraper(soup, config):
    return Scraper(soup, config)


@pytest.fixture(name="request_params")
def request_params_():
    date_ = datetime.date(2023, 11, 4)
    category = "wirtschaft"
    archive_filter = ArchiveFilter(date_, category)
    return create_request_params(archive_filter)
