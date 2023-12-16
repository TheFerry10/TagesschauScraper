import os
import shutil
import unittest
from datetime import date, datetime

import pytest
from bs4 import BeautifulSoup

from tagesschauscraper import archive, helper


class TestDateDirectoryTreeCreator(unittest.TestCase):
    def setUp(self) -> None:
        date_ = date(2022, 1, 12)
        root_dir = "tests/tmp"
        self.date_ = date_
        self.root_dir = root_dir
        if os.path.isdir(root_dir):
            shutil.rmtree(self.root_dir)
        os.makedirs(root_dir, exist_ok=True)
        self.dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(
            date_=date_, date_pattern="%Y/%m", root_dir=root_dir
        )
        self.true_file_path = os.path.join(root_dir, "2022/01")

    def tearDown(self) -> None:
        shutil.rmtree(self.root_dir)

    def test_create_file_path_from_date(self) -> None:
        self.assertEqual(
            self.true_file_path,
            self.dateDirectoryTreeCreator.create_file_path_from_date(),
        )

    def test_make_dir_tree_from_date(self) -> None:
        self.dateDirectoryTreeCreator.make_dir_tree_from_date()
        self.assertTrue(self.true_file_path)

    def test_make_dir_tree_from_file_path(self) -> None:
        self.dateDirectoryTreeCreator.make_dir_tree_from_file_path(self.true_file_path)
        self.assertTrue(self.true_file_path)


class TestCreateFileNameFromDate(unittest.TestCase):
    def test_create_file_name_from_date(self) -> None:
        date_ = date(2022, 1, 12)
        true_file_name = "prefix_2022-01-12_suffix.json"
        self.assertEqual(
            true_file_name,
            helper.create_file_name_from_date(
                date_, prefix="prefix_", suffix="_suffix", extension=".json"
            ),
        )

    def test_create_file_name_from_datetime(self) -> None:
        datetime_ = datetime(2022, 1, 12, 11, 12, 30)
        true_file_name = "prefix_2022-01-12T11:12:30_suffix.json"
        self.assertEqual(
            true_file_name,
            helper.create_file_name_from_date(
                datetime_,
                prefix="prefix_",
                suffix="_suffix",
                extension=".json",
            ),
        )


class TestNormalizeDatetime(unittest.TestCase):
    def test_normalize_datetime(self) -> None:
        self.assertEqual(
            helper.transform_datetime_str("30.01.2021 - 18:04 Uhr"),
            "2021-01-30 18:04:00",
        )


class TestDateRange(unittest.TestCase):
    def test_get_date_range(self) -> None:
        expected_result = [
            date(2022, 1, 1),
            date(2022, 1, 2),
            date(2022, 1, 3),
            date(2022, 1, 4),
        ]
        self.assertListEqual(
            helper.get_date_range(date(2022, 1, 1), date(2022, 1, 5)),
            expected_result,
        )


def test_creation_of_valid_request_params():
    expected_params = {"datum": "2023-02-04", "filter": "wirtschaft"}
    archiveFilter = archive.ArchiveFilter(date(2023, 2, 4), "wirtschaft")
    request_params = archive.create_request_params(archiveFilter)
    assert request_params == expected_params


def test_creation_of_valid_request_params_category_is_none():
    expected_params = {"datum": "2023-02-04", "filter": None}
    archiveFilter = archive.ArchiveFilter(date(2023, 2, 4), None)
    request_params = archive.create_request_params(archiveFilter)
    assert request_params == expected_params


def test_creation_of_invalid_request_params():
    archiveFilter = archive.ArchiveFilter(date(2023, 2, 4), "invalidCategory")
    with pytest.raises(Exception):
        archive.create_request_params(archiveFilter)


def test_clean_string():
    input_string = " test      \nthis\n  thing        "
    expected_clean_string = "test this thing"
    cleaned_string = helper.clean_string(input_string)
    assert cleaned_string == expected_clean_string


def test_extract_link_from_tag():
    expected_link = "/test/url/sample.html"
    html_with_link = f'<a class="link" href={expected_link}>'
    tag_with_link = BeautifulSoup(html_with_link, "html.parser").a
    link = helper.extract_link(tag_with_link)  # type: ignore
    assert link == expected_link


def test_extract_text_from_tag():
    expected_text = "This is /n some sample text!  "
    html_with_text = f'<span class="text">{expected_text}</span>'
    tag_with_text = BeautifulSoup(html_with_text, "html.parser").span
    text = helper.extract_text(tag_with_text)  # type: ignore
    assert text == expected_text
