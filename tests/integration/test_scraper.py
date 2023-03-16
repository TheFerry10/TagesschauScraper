import json
import unittest
import requests
from datetime import date
from tagesschauscraper import tagesschau


class TestTagesschauScraper(unittest.TestCase):
    def setUp(self) -> None:
        dates = [date(2023, 3, 1), date(2023, 3, 2)]
        category = "wirtschaft"
        self.archiveFilters = [
            tagesschau.ArchiveFilter({"date": d, "category": category})
            for d in dates
        ]
        self.config = tagesschau.ScraperConfig(self.archiveFilters)
        self.tageschauScraper = tagesschau.TagesschauScraper()

    def test_scraper_config(self) -> None:
        expected_request_parameter_list = [
            {"datum": "2023-03-01", "ressort": "wirtschaft", "pageIndex": "1"},
            {"datum": "2023-03-02", "ressort": "wirtschaft", "pageIndex": "1"},
        ]
        self.assertListEqual(
            self.config.request_params, expected_request_parameter_list
        )

    def test_get_news_from_archive(self) -> None:
        with open(
            "tests/data/teaser-article-2023-03-01-2023-03-02.json", "r"
        ) as f:
            expected_records = json.load(f)
        self.assertDictEqual(
            self.tageschauScraper.get_news_from_archive(self.config),
            expected_records,
        )

    def test_scrape_teaser_and_articles(self) -> None:
        with open("tests/data/teaser-article-2023-01-01.json", "r") as f:
            expected_records = json.load(f)
        response = requests.get(
            "https://www.tagesschau.de/archiv/", params={"datum": "2023-01-01"}
        )
        self.assertDictEqual(
            self.tageschauScraper.scrape_teaser_and_articles(response),
            expected_records,
        )

    def test_scrape_teaser(self) -> None:
        with open("tests/data/teaser-2023-01-01.json", "r") as f:
            expected_records = json.load(f)
        response = requests.get(
            "https://www.tagesschau.de/archiv/", params={"datum": "2023-01-01"}
        )
        self.assertDictEqual(
            self.tageschauScraper.scrape_teaser(response), expected_records
        )
