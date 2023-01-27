import unittest
from tagesschauscraper.helper import transform_datetime_str


class TestNormalizeDatetime(unittest.TestCase):
    def test_normalize_datetime(self):
        self.assertEqual(
            transform_datetime_str("30.01.2021 - 18:04 Uhr"), "2021-01-30 18:04:00"
        )


if __name__ == "__main__":
    unittest.main()
