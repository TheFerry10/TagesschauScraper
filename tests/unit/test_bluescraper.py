from unittest.mock import patch

import pytest

from bluescraper import constants
from bluescraper.config import (
    Config,
    ConfigReader,
    ScrapingConfig,
    TagScrapingConfig,
)
from bluescraper.constants import DEFAULT_TIMEOUT
from bluescraper.scraper import Scraper
from bluescraper.utils import TagDefinition, get_html, get_soup
from bluescraper.validation import (
    ExistingStringInTag,
    SoapValidator,
    ValidationConfig,
)


def test_loading_config_from_file():
    tags = [
        TagScrapingConfig(
            id=id,
            content_type=content_type,
            tag=TagDefinition(name=name, attrs=attrs),
        )
        for id, content_type, name, attrs in [
            ("article_link", "href", None, {"class": "teaser-right__link"}),
            ("topline", None, None, {"class": "teaser-right__labeltopline"}),
            ("headline", None, None, {"class": "teaser-right__headline"}),
            ("shorttext", None, None, {"class": "teaser-right__shorttext"}),
            ("date", None, None, {"class": "teaser-right__date"}),
        ]
    ]
    scraping = ScrapingConfig(tags=tags)

    existing_tags = [
        TagDefinition(name=name, attrs=attrs)
        for name, attrs in [
            ("div", {"class": "teaser-right twelve"}),
            ("span", {"class": "teaser-right__labeltopline"}),
        ]
    ]

    existing_strings_in_tags = [
        ExistingStringInTag(
            include_string=include_string,
            tag=TagDefinition(name=name, attrs=attrs),
        )
        for include_string, name, attrs in [
            ("headline", "span", {"class": "teaser-right__headline"}),
            ("Test topline", "span", {"class": "teaser-right__labeltopline"}),
        ]
    ]

    validation = ValidationConfig(
        existing_tags=existing_tags,
        existing_strings_in_tags=existing_strings_in_tags,
    )
    expected_config = Config(scraping=scraping, validation=validation)
    filepath = constants.TEST_CONFIG_DIR.joinpath("config.yml")
    config_reader = ConfigReader(filepath)
    config = config_reader.load()
    assert config == expected_config


def test_loading_config_from_file_without_validation():
    tags = [
        TagScrapingConfig(
            id=id,
            content_type=content_type,
            tag=TagDefinition(name=name, attrs=attrs),
        )
        for id, content_type, name, attrs in [
            ("article_link", "href", None, {"class": "teaser-right__link"}),
            ("topline", "text", None, {"class": "teaser-right__labeltopline"}),
            ("headline", "text", None, {"class": "teaser-right__headline"}),
            ("shorttext", "text", None, {"class": "teaser-right__shorttext"}),
            ("date", "text", None, {"class": "teaser-right__date"}),
        ]
    ]
    scraping = ScrapingConfig(tags=tags)
    expected_config = Config(scraping=scraping)
    filepath = constants.TEST_CONFIG_DIR.joinpath("config-no-validation.yml")
    config_reader = ConfigReader(filepath)
    config = config_reader.load()
    assert config == expected_config


def test_reading_scraper_config_from_yaml():
    filepath = constants.TEST_CONFIG_DIR.joinpath("config.yml")
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
        "scraping": {
            "tags": [
                {
                    "id": "article_link",
                    "content_type": "href",
                    "tag": {
                        "name": None,
                        "attrs": {"class": "teaser-right__link"},
                    },
                },
                {
                    "id": "topline",
                    "content_type": None,
                    "tag": {
                        "name": None,
                        "attrs": {"class": "teaser-right__labeltopline"},
                    },
                },
                {
                    "id": "headline",
                    "content_type": None,
                    "tag": {
                        "name": None,
                        "attrs": {"class": "teaser-right__headline"},
                    },
                },
                {
                    "id": "shorttext",
                    "content_type": None,
                    "tag": {
                        "name": None,
                        "attrs": {"class": "teaser-right__shorttext"},
                    },
                },
                {
                    "id": "date",
                    "content_type": None,
                    "tag": {
                        "name": None,
                        "attrs": {"class": "teaser-right__date"},
                    },
                },
            ]
        },
    }
    assert config_raw == expected


def test_reading_scraper_config_from_json():
    filepath = constants.TEST_CONFIG_DIR.joinpath("config.json")
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
                "content_type": "href",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__link"},
                },
            },
            {
                "id": "topline",
                "content_type": "text",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__labeltopline"},
                },
            },
            {
                "id": "headline",
                "content_type": "text",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__headline"},
                },
            },
            {
                "id": "shorttext",
                "content_type": "text",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__shorttext"},
                },
            },
            {
                "id": "date",
                "content_type": "text",
                "tag": {
                    "name": None,
                    "attrs": {"class": "teaser-right__date"},
                },
            },
        ],
    }
    assert config_raw == expected


@pytest.mark.parametrize(
    argnames="html, expected",
    argvalues=[
        pytest.param(
            constants.TEST_HTML_DIR.joinpath("valid.html"),
            True,
            id="valid html",
        ),
        pytest.param(
            constants.TEST_HTML_DIR.joinpath("invalid.html"),
            False,
            id="invalid html",
        ),
    ],
    indirect=["html"],
)
def test_validate_html(soup, expected):
    existing_tags = [
        TagDefinition(name="div", attrs={"class": "teaser-right twelve"})
    ]
    validation_content = ValidationConfig(existing_tags=existing_tags)
    validator = SoapValidator(soup, validation_content)
    validator.validate()
    assert validator.valid == expected


@pytest.mark.parametrize(
    "html", [constants.TEST_HTML_DIR.joinpath("valid.html")], indirect=True
)
@patch("bluescraper.utils.requests.get")
def test_get_html(mock_requests_get, html):
    mock_requests_get.return_value.ok = True
    mock_requests_get.return_value.text = html
    html_ = get_html(
        url="https://example.com/", request_params={"parameter": "value"}
    )
    mock_requests_get.assert_called_once_with(
        url="https://example.com/",
        params={"parameter": "value"},
        timeout=DEFAULT_TIMEOUT,
    )
    assert html == html_


@pytest.mark.parametrize(
    "html", [constants.TEST_HTML_DIR.joinpath("valid.html")], indirect=True
)
@patch("bluescraper.utils.requests.get")
def test_get_soup(mock_requests_get, soup, html):
    mock_requests_get.return_value.ok = True
    mock_requests_get.return_value.text = html
    soup_ = get_soup(
        url="https://example.com/", request_params={"parameter": "value"}
    )
    mock_requests_get.assert_called_once_with(
        url="https://example.com/",
        params={"parameter": "value"},
        timeout=DEFAULT_TIMEOUT,
    )
    assert soup == soup_


def test_scraper_service_e2e():
    soup = get_soup(
        "https://www.tagesschau.de/archiv",
        request_params={"datum": "2024-02-08", "filter": "inland"},
    )
    config_reader = ConfigReader(constants.CONFIG_YAML)
    config = config_reader.load()
    if soup:
        scraper = Scraper(soup, config)
        results = scraper.extract()
    assert False
