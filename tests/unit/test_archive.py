from tagesschauscraper import archive
from bs4 import BeautifulSoup
import pytest
from pathlib import Path


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
def archive_date():
    file_name = "date.html"
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


@pytest.mark.parametrize(
    "archive_html", ["teaser_container.html"], indirect=True
)
def test_extract_teaser_list(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.Archive(soup)
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
    archive_ = archive.Archive(soup)
    assert archive_.valid == is_valid


@pytest.mark.parametrize("archive_html", ["date.html"], indirect=True)
def test_extract_date(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.Archive(soup)
    expected_date: str = "1. Oktober 2023"
    assert archive_.extract_date() == expected_date


@pytest.mark.parametrize(
    "archive_html", ["news_categories.html"], indirect=True
)
def test_extract_news_categories(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    archive_ = archive.Archive(soup)
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


@pytest.mark.parametrize("archive_html", ["valid_header.html"], indirect=True)
def test_is_tag_in_soup(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    tag_definition = archive.TagDefinition(
        "div", {"class": "trenner__text__topline"}
    )
    assert archive.is_tag_in_soup(soup, tag_definition)


@pytest.mark.parametrize("archive_html", ["valid_header.html"], indirect=True)
def test_is_text_in_tag(archive_html):
    soup = BeautifulSoup(archive_html, "html.parser")
    tag_definition = archive.TagDefinition(
        "div", {"class": "trenner__text__topline"}
    )
    example_text = "Archiv"
    assert archive.is_text_in_tag(soup, tag_definition, example_text)


def test_if_available_category_is_recognized():
    assert archive.is_selected_in_categories("wirtschaft")


def test_if_not_available_category_leads_to_false():
    assert not archive.is_selected_in_categories("test category")
