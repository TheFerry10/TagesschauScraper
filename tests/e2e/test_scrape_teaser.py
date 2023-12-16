import datetime
from pathlib import Path
from typing import Dict, List
from unittest.mock import patch

import pytest

from tagesschauscraper.archive import ArchiveFilter
from tagesschauscraper.domain import scrape_teaser

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
    expected_teaser_list = [
        {
            "DATE": "04.11.2023 • 15:41 Uhr",
            "TOPLINE": "Tipps für die kalte Jahreszeit",
            "HEADLINE": "So macht man sein Auto winterfest",
            "SHORTTEXT": "Bei vielen Autos sind die Scheinwerfer falsch eingestellt - was ab Herbst besonders gefährlich sein kann. Worauf sollte man außerdem achten? Experten-Tipps für den Winter-Check. Von Hannah Stumpf. mehr",
            "ARTICLE_LINK": "/wirtschaft/verbraucher/auto-winter-licht-check-100.html",
            "EXTRACTION_TIMESTAMP": None,
        }
    ]
    archive_filter = ArchiveFilter(
        date=datetime.date(2023, 11, 4), news_category="wirtschaft"
    )
    teaser_list = scrape_teaser(archive_filter)
    assert expected_teaser_list == remove_extraction_timestamp(teaser_list)


def remove_extraction_timestamp(teaser_list: List[Dict]):
    for t in teaser_list:
        t["EXTRACTION_TIMESTAMP"] = None
    return teaser_list
