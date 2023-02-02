import os
import shutil
import unittest
import datetime
from tagesschauscraper import helper


class TestDateDirectoryTreeCreator(unittest.TestCase):
    def setUp(self) -> None:
        date_ = datetime.date(2022, 1, 12)
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

    def test_create_file_path_from_date(self):
        self.assertEqual(
            self.true_file_path,
            self.dateDirectoryTreeCreator.create_file_path_from_date(),
        )

    def test_make_dir_tree_from_date(self):
        self.dateDirectoryTreeCreator.make_dir_tree_from_date()
        self.assertTrue(self.true_file_path)

    def test_make_dir_tree_from_file_path(self):
        self.dateDirectoryTreeCreator.make_dir_tree_from_file_path(
            self.true_file_path
        )
        self.assertTrue(self.true_file_path)


class TestCreateFileNameFromDate(unittest.TestCase):
    def test_create_file_name_from_date(self):
        date_ = datetime.date(2022, 1, 12)
        true_file_name = "prefix_2022-01-12_suffix.json"
        self.assertEqual(
            true_file_name,
            helper.create_file_name_from_date(
                date_, prefix="prefix_", suffix="_suffix", extension=".json"
            ),
        )

    def test_create_file_name_from_datetime(self):
        datetime_ = datetime.datetime(2022, 1, 12, 11, 12, 30)
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
    def test_normalize_datetime(self):
        self.assertEqual(
            helper.transform_datetime_str("30.01.2021 - 18:04 Uhr"),
            "2021-01-30 18:04:00",
        )


if __name__ == "__main__":
    unittest.main()
