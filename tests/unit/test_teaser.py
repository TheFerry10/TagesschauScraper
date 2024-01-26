from pathlib import Path
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper.domain import teaser
from tagesschauscraper.domain.constants import TEASER_TEST_DATA_DIR
from tagesschauscraper.domain.helper import (
    ConfigReader,
    TagDefinition,
    ValidationContent,
    extract_link,
    extract_text,
    SoapValidator,
    Config,
)
from tagesschauscraper.domain.teaser import Teaser


@pytest.fixture(name="teaser_html")
def teaser_html_(request):
    file_name = request.param
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="invalid_teaser_html")
def invalid_teaser_html_():
    file_name = "invalid-teaser.html"
    with open(
        TEASER_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8"
    ) as f:
        content = f.read()
    return content


@pytest.fixture(name="valid_teaser_html")
def valid_teaser_html_():
    file_name = "valid-teaser.html"
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

    teaser_config_path = Path("tests/data/config/teaser-config.yml")
    config_reader = ConfigReader(teaser_config_path)
    teaser_config = config_reader.load()
    return teaser.TeaserScraper(soup, teaser_config)


def test_loading_config_from_file():
    scraping = {
        "article_link": TagDefinition(attrs={"class": "teaser-right__link"}),
        "topline": TagDefinition(
            attrs={"class": "teaser-right__labeltopline"}
        ),
        "headline": TagDefinition(attrs={"class": "teaser-right__headline"}),
        "shorttext": TagDefinition(attrs={"class": "teaser-right__shorttext"}),
        "date": TagDefinition(attrs={"class": "teaser-right__date"}),
    }
    existing_tags = [
        TagDefinition(name, attrs)
        for name, attrs in [
            ("div", {"class": "teaser-right twelve"}),
            ("span", {"class": "teaser-right__labeltopline"}),
        ]
    ]
    existing_strings_in_tags = [
        (
            "headline",
            TagDefinition(
                name="span", attrs={"class": "teaser-right__headline"}
            ),
        ),
        (
            "Test topline",
            TagDefinition(
                name="span", attrs={"class": "teaser-right__labeltopline"}
            ),
        ),
    ]
    validation = ValidationContent(existing_tags, existing_strings_in_tags)
    expected_config = Config(scraping=scraping, validation=validation)

    filepath = Path("tests/data/config/teaser-config.yml")
    config_reader = ConfigReader(filepath)
    config = config_reader.load()
    assert config == expected_config


def test_loading_config_from_file_without_validation():
    scraping = {
        "article_link": TagDefinition(attrs={"class": "teaser-right__link"}),
        "topline": TagDefinition(
            attrs={"class": "teaser-right__labeltopline"}
        ),
        "headline": TagDefinition(attrs={"class": "teaser-right__headline"}),
        "shorttext": TagDefinition(attrs={"class": "teaser-right__shorttext"}),
        "date": TagDefinition(attrs={"class": "teaser-right__date"}),
    }

    validation = ValidationContent(
        existing_tags=[], existing_strings_in_tags=[]
    )
    expected_config = Config(scraping=scraping, validation=validation)

    filepath = Path("tests/data/config/teaser-config-no-validation.yml")
    config_reader = ConfigReader(filepath)
    config = config_reader.load()
    assert config == expected_config


def test_reading_scraper_config_from_yaml():
    filepath = Path("tests/data/config/teaser-config.yml")
    config_reader = ConfigReader(filepath)
    config_raw = config_reader.read()
    expected = {
        "validation": {
            "existing_tags": [
                {"name": "div", "attrs": {"class": "teaser-right twelve"}},
                {
                    "name": "span",
                    "attrs": {"class": "teaser-right__labeltopline"},
                },
            ],
            "existing_strings_in_tags": [
                {
                    "include_string": "headline",
                    "tag": {
                        "name": "span",
                        "attrs": {"class": "teaser-right__headline"},
                    },
                },
                {
                    "include_string": "Test topline",
                    "tag": {
                        "name": "span",
                        "attrs": {"class": "teaser-right__labeltopline"},
                    },
                },
            ],
        },
        "scraping": [
            {
                "id": "article_link",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__link"},
                },
            },
            {
                "id": "topline",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__labeltopline"},
                },
            },
            {
                "id": "headline",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__headline"},
                },
            },
            {
                "id": "shorttext",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__shorttext"},
                },
            },
            {
                "id": "date",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__date"},
                },
            },
        ],
    }
    assert config_raw == expected


def test_reading_scraper_config_from_json():
    filepath = Path("tests/data/config/teaser-config.json")
    configReader = ConfigReader(filepath)
    config_raw = configReader.read()
    expected = {
        "validation": {
            "existing_tags": [
                {"name": "div", "attrs": {"class": "teaser-right twelve"}},
                {
                    "name": "span",
                    "attrs": {"class": "teaser-right__labeltopline"},
                },
            ],
            "existing_strings_in_tags": [
                {
                    "include_string": "headline",
                    "tag": {
                        "name": "span",
                        "attrs": {"class": "teaser-right__headline"},
                    },
                },
                {
                    "include_string": "Test topline",
                    "tag": {
                        "name": "span",
                        "attrs": {"class": "teaser-right__labeltopline"},
                    },
                },
            ],
        },
        "scraping": [
            {
                "id": "article_link",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__link"},
                },
            },
            {
                "id": "topline",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__labeltopline"},
                },
            },
            {
                "id": "headline",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__headline"},
                },
            },
            {
                "id": "shorttext",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__shorttext"},
                },
            },
            {
                "id": "date",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__date"},
                },
            },
        ],
    }
    assert config_raw == expected


def test_extract_link_to_article(valid_teaser):
    expected_link_to_article = "/dummy/article.html"
    link_to_article = valid_teaser.extract_tag(
        valid_teaser.config.scraping["article_link"], extract_link
    )
    assert expected_link_to_article == link_to_article


def test_extract_topline(valid_teaser):
    expected_topline = "Test topline"
    topline = valid_teaser.extract_tag(
        valid_teaser.config.scraping["topline"], extract_text
    )
    assert topline == expected_topline


def test_extract_headline(valid_teaser):
    expected_headline = "Test headline"
    headline = valid_teaser.extract_tag(
        valid_teaser.config.scraping["headline"], extract_text
    )
    assert headline == expected_headline


def test_extract_shorttext(valid_teaser):
    expected_shorttext = "Test short text"
    shorttext = valid_teaser.extract_tag(
        valid_teaser.config.scraping["shorttext"], extract_text
    )
    assert shorttext == expected_shorttext


def test_extract_date(valid_teaser):
    expected_date = "08.10.2023 • 13:17 Uhr"
    topline = valid_teaser.extract_tag(
        valid_teaser.config.scraping["date"], extract_text
    )
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
    assert valid_teaser.can_scrape()
    teaser_ = valid_teaser.extract()
    assert teaser_ == expectedTeaser


def test_validation_for_valid_html_teaser(valid_teaser_html):
    soup = BeautifulSoup(valid_teaser_html, "html.parser")
    existing_tags = [TagDefinition("div", {"class": "teaser-right twelve"})]
    validation_content = ValidationContent(
        existing_tags, existing_strings_in_tags=[]
    )
    validator = SoapValidator(soup, validation_content)
    validator.validate()
    assert validator.valid


def test_validation_for_invalid_html_teaser(invalid_teaser_html):
    soup = BeautifulSoup(invalid_teaser_html, "html.parser")
    existing_tags = [TagDefinition("div", {"class": "teaser-right twelve"})]
    validation_content = ValidationContent(
        existing_tags, existing_strings_in_tags=[]
    )
    validator = SoapValidator(soup, validation_content)
    validator.validate()
    assert not validator.valid
