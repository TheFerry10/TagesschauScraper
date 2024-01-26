from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper.domain import archive

# 1. version
#     Write the test data explicitly in the tests
# 2. version
#     Write the test data in files and import the content in the tests.
#     Sometimes redundant work because the same code for importing is written
#     for a couple of tests.
# 3. Create fixture with loading the data to the test. One fixture for one
#     file. Also a lot of redundant code
# 4. Use indirect parameterization: Combine parameterize and fixture decorator to come up with a clean and
#     readable solution (https://docs.pytest.org/en/latest/example/parametrize.html#apply-indirect-on-particular-arguments)


ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")


@pytest.mark.parametrize(
    "archive_html", ["teaser_container.html"], indirect=True
)
def test_extract_teaser_list(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.ArchiveScraper(soup)
    teaser_list = archive_.extract_teaser_list()
    teaser_dates = [t.get("data-teaserdate") for t in teaser_list]
    expected_teaser_dates = [
        "1694725289",
        "1694725238",
        "1694723576",
        "1694716345",
        "1694716177",
    ]
    assert len(teaser_list) == 5
    assert teaser_dates == expected_teaser_dates


@pytest.mark.parametrize(
    "archive_html,is_valid",
    [
        pytest.param("valid_header.html", True, id="valid"),
        pytest.param("invalid_header.html", False, id="invalid"),
    ],
    indirect=["archive_html"],
)
def test_archive_with_input(archive_html, is_valid):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.ArchiveScraper(soup)
    assert archive_.valid == is_valid


@pytest.mark.parametrize("archive_html", ["date.html"], indirect=True)
def test_extract_date(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.ArchiveScraper(soup)
    expected_date: str = "1. Oktober 2023"
    assert archive_.extract_date() == expected_date


@pytest.mark.parametrize(
    "archive_html", ["news_categories.html"], indirect=True
)
def test_extract_news_categories(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.ArchiveScraper(soup)
    expected_categories = {
        "Alle\n                Ressorts",
        "Inland",
        "Ausland",
        "Wirtschaft",
        "Wissen",
        "Faktenfinder",
        "Investigativ",
    }
    assert archive_.extract_news_categories() == expected_categories


def test_if_available_category_is_recognized():
    assert archive.is_selected_in_categories("wirtschaft")


def test_if_not_available_category_leads_to_false():
    assert not archive.is_selected_in_categories("test category")
    assert not archive.is_selected_in_categories("test category")
