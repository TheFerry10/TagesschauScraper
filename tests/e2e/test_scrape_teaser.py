import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from tagesschauscraper.archive import ArchiveFilter
from tagesschauscraper.service import scrape_teaser
from tagesschauscraper.teaser import Teaser

ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")


@pytest.fixture(name="expected_archive_html")
def archive_html():
    file_name = "archive-20231104-wirtschaft.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@patch("tagesschauscraper.archive.requests.get")
def test_scrape_all_teaser_for_date(mock_get, expected_archive_html):
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_archive_html
    expected_teaser = Teaser(
        date="04.11.2023 • 15:41 Uhr",
        topline="Tipps für die kalte Jahreszeit",
        headline="So macht man sein Auto winterfest",
        shorttext=(
            "Bei vielen Autos sind die Scheinwerfer falsch eingestellt - was"
            " ab Herbst besonders gefährlich sein kann. Worauf sollte man"
            " außerdem achten? Experten-Tipps für den Winter-Check. Von Hannah"
            " Stumpf. mehr"
        ),
        article_link=("/wirtschaft/verbraucher/auto-winter-licht-check-100.html"),
        extraction_timestamp="2023-01-01T00:00:00",
    )
    expected_teaser_list = [expected_teaser]
    archive_filter = ArchiveFilter(
        date=datetime.date(2023, 11, 4), news_category="wirtschaft"
    )
    teaser_list = scrape_teaser(
        archive_filter, extraction_timestamp=datetime.datetime(2023, 1, 1)
    )
    assert expected_teaser_list == teaser_list
