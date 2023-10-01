from tagesschauscraper import tagesschau
from datetime import date
from bs4 import BeautifulSoup
import pytest
from pathlib import Path


ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")


@pytest.fixture
def archive_valid_header():
    file_name = "valid_header.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def archive_invalid_header():
    file_name = "invalid_header.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def archive_date():
    file_name = "date.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def archive_news_categories():
    file_name = "news_categories.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def archive_teaser_container():
    file_name = "teaser_container.html"
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def archive_html(request):
    file_name = request.param
    with open(ARCHIVE_TEST_DATA_DIR.joinpath(file_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content


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
    archive = tagesschau.Archive(soup)
    assert archive.valid == is_valid


@pytest.mark.parametrize("archive_html", [("date.html")], indirect=True)
def test_extract_date(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive = tagesschau.Archive(soup)
    expected_date: str = "1. Oktober 2023"
    assert archive.extract_date() == expected_date


@pytest.mark.parametrize("archive_html", [("news_categories.html")], indirect=True)
def test_extract_news_categories(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive = tagesschau.Archive(soup)
    expected_categories = {
        "Alle\n                Ressorts",
        "Inland",
        "Ausland",
        "Wirtschaft",
        "Wissen",
        "Faktenfinder",
        "Investigativ",
    }
    assert archive.extract_news_categories() == expected_categories


# def test_extract_


@pytest.mark.parametrize("archive_html", [("valid_header.html")], indirect=True)
def test_is_tag_in_soup(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    tag_definition = tagesschau.TagDefinition(
        "div", {"class": "trenner__text__topline"}
    )
    assert tagesschau.is_tag_in_soup(soup, tag_definition)


@pytest.mark.parametrize("archive_html", [("valid_header.html")], indirect=True)
def test_is_text_in_tag(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    tag_definition = tagesschau.TagDefinition(
        "div", {"class": "trenner__text__topline"}
    )
    example_text = "Archiv"
    assert tagesschau.is_text_in_tag(soup, tag_definition, example_text)


def test_if_available_category_is_recognized():
    assert tagesschau.is_selected_in_categories("wirtschaft")


def test_if_not_available_category_leads_to_false():
    assert not tagesschau.is_selected_in_categories("test category")


def test_creation_of_request_params():
    expected_params = {"datum": "2023-02-04", "filter": "wirtschaft"}
    archiveFilter = tagesschau.ArchiveFilter(date(2023, 2, 4), "wirtschaft")
    request_params = tagesschau.create_request_params(archiveFilter)
    assert request_params == expected_params
