import datetime
import os

import pytest
from bs4 import BeautifulSoup
from bluescraper.fileutils import (
    DateDirectoryTreeCreator,
    create_file_name_from_date,
)
from bluescraper.utils import (
    clean_string,
    extract_text,
    get_date_range,
    is_tag_in_soup,
    is_text_in_tag,
    transform_datetime_str,
)

from tagesschau.domain.archive import (
    TagDefinition,
)
from bluescraper.validation import (
    ExistingStringInTag,
    SoapValidator,
    ValidationConfig,
)
from tagesschau.domain.helper import (
    extract_link,
)
from tagesschau.domain.model import ArchiveFilter, create_request_params


def test_create_file_path_from_date(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    assert (
        true_file_path == dateDirectoryTreeCreator.create_file_path_from_date()
    )


def test_make_dir_tree_from_date(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    dateDirectoryTreeCreator.make_dir_tree_from_date()
    assert true_file_path


def test_make_dir_tree_from_file_path(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    dateDirectoryTreeCreator.make_dir_tree_from_file_path(true_file_path)
    assert true_file_path


def test_create_file_name_from_date() -> None:
    date_ = datetime.date(2022, 1, 12)
    true_file_name = "prefix_2022-01-12_suffix.json"
    assert true_file_name == create_file_name_from_date(
        date_, prefix="prefix_", suffix="_suffix", extension=".json"
    )


def test_create_file_name_from_datetime() -> None:
    datetime_ = datetime.datetime(2022, 1, 12, 11, 12, 30)
    true_file_name = "prefix_2022-01-12T11:12:30_suffix.json"
    assert true_file_name == create_file_name_from_date(
        datetime_, prefix="prefix_", suffix="_suffix", extension=".json"
    )


def test_normalize_datetime() -> None:
    assert (
        transform_datetime_str("30.01.2021 - 18:04 Uhr")
        == "2021-01-30 18:04:00"
    )


def test_get_date_range() -> None:
    expected_result = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]
    assert (
        get_date_range(datetime.date(2022, 1, 1), datetime.date(2022, 1, 5))
        == expected_result
    )


def test_creation_of_valid_request_params():
    expected_params = {"datum": "2023-02-04", "filter": "wirtschaft"}
    archiveFilter = ArchiveFilter(datetime.date(2023, 2, 4), "wirtschaft")
    request_params = create_request_params(archiveFilter)
    assert request_params == expected_params


def test_creation_of_valid_request_params_category_is_none():
    expected_params = {"datum": "2023-02-04", "filter": None}
    archiveFilter = ArchiveFilter(datetime.date(2023, 2, 4), None)
    request_params = create_request_params(archiveFilter)
    assert request_params == expected_params


def test_creation_of_invalid_request_params():
    archiveFilter = ArchiveFilter(datetime.date(2023, 2, 4), "invalidCategory")
    with pytest.raises(Exception):
        create_request_params(archiveFilter)


def test_clean_string():
    input_string = " test      \nthis\n  thing        "
    expected_clean_string = "test this thing"
    cleaned_string = clean_string(input_string)
    assert cleaned_string == expected_clean_string


def test_extract_link_from_tag():
    expected_link = "/test/url/sample.html"
    html_with_link = f'<a class="link" href={expected_link}>'
    tag_with_link = BeautifulSoup(html_with_link, "html.parser").a
    link = extract_link(tag_with_link)  # type: ignore
    assert link == expected_link


def test_extract_text_from_tag():
    expected_text = "This is /n some sample text!"
    html_with_text = f'<span class="text">{expected_text}</span>'
    tag_with_text = BeautifulSoup(html_with_text, "html.parser").span
    text = extract_text(tag_with_text)  # type: ignore
    assert text == expected_text


def test_is_text_in_tag(valid_teaser):
    tag_definition = TagDefinition(
        name="span", attrs={"class": "teaser-right__labeltopline"}
    )
    example_text = " topline"
    assert is_text_in_tag(valid_teaser, tag_definition, example_text)


def test_is_tag_in_soup(valid_teaser):
    tag_definition = TagDefinition(
        name="span", attrs={"class": "teaser-right__headline"}
    )
    assert is_tag_in_soup(valid_teaser, tag_definition)


def test_validator_with_validation_content(valid_teaser):
    existing_tags = [
        TagDefinition(name=name, attrs=attrs)
        for name, attrs in [
            ("span", {"class": "teaser-right__labeltopline"}),
            ("span", {"class": "teaser-right__headline"}),
            (None, {"class": "teaser-right__shorttext"}),
        ]
    ]
    existing_strings_in_tags = [
        ExistingStringInTag(
            include_string=include_string,
            tag=TagDefinition(name=name, attrs=attrs),
        )
        for include_string, name, attrs in [
            ("Test topline", "span", {"class": "teaser-right__labeltopline"}),
            ("headline", "span", {"class": "teaser-right__headline"}),
        ]
    ]

    validation_config = ValidationConfig(
        existing_tags=existing_tags,
        existing_strings_in_tags=existing_strings_in_tags,
    )
    validator = SoapValidator(valid_teaser, validation_config)
    validator.validate()
    assert validator.valid
