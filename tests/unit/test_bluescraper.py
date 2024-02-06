from pathlib import Path

from bs4 import BeautifulSoup

from bluescraper.config import (
    Config,
    ConfigReader,
    ScrapingConfig,
    TagScrapingConfig,
)
from bluescraper.utils import TagDefinition
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

    filepath = Path("tests/data/config/teaser-config.yml")
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
    filepath = Path("tests/data/config/teaser-config.json")
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


def test_validation_for_valid_html_teaser(valid_teaser_html):
    soup = BeautifulSoup(valid_teaser_html, "html.parser")
    existing_tags = [
        TagDefinition(name="div", attrs={"class": "teaser-right twelve"})
    ]
    validation_content = ValidationConfig(existing_tags=existing_tags)
    validator = SoapValidator(soup, validation_content)
    validator.validate()
    assert validator.valid


def test_validation_for_invalid_html_teaser(invalid_teaser_html):
    soup = BeautifulSoup(invalid_teaser_html, "html.parser")
    existing_tags = [
        TagDefinition(name="div", attrs={"class": "teaser-right twelve"})
    ]
    validation_content = ValidationConfig(existing_tags=existing_tags)
    validator = SoapValidator(soup, validation_content)
    validator.validate()
    assert not validator.valid
