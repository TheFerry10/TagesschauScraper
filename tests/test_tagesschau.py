import json
import unittest
from datetime import date

import requests

from scraping.helper import transform_datetime_str
from scraping.retrieve import get_soup
from scraping.tagesschau import TagesschauScraper


class TestTagesschauScraper(unittest.TestCase):
    def setUp(self):  
        self.tageschauScraper = TagesschauScraper()
        self.url = "https://www.tagesschau.de/archiv/?datum=2022-03-01&ressort=wirtschaft"
        response = requests.get(url=self.url)
        self.soup = get_soup(response)
        with open("data/sample.html", "r") as f:
            self.html = f.read()
    #     with open("data/news/tagesschau/test_teasers.json", "r") as f:
    #         self.test_teasers = json.load(f)
    
    def test_create_url_for_news_archive(self):
        self.assertEqual(
            self.tageschauScraper.create_url_for_news_archive(date(2020,1,1), 'wirtschaft'),
            "https://www.tagesschau.de/archiv/?datum=2020-01-01&ressort=wirtschaft"
            )
        self.assertEqual(
            self.tageschauScraper.create_url_for_news_archive(date(2020,1,1), 'inland'),
            "https://www.tagesschau.de/archiv/?datum=2020-01-01&ressort=inland"
            )
        with self.assertRaises(ValueError):
            self.tageschauScraper.create_url_for_news_archive(date(2020,1,1), 'foo')
    
    def test_archive_headline(self):
        archive_headline = self.tageschauScraper.get_archive_headline(self.soup)
        self.assertEqual(archive_headline, "1. März 2022")
        
    def test_is_url_valid(self):
        self.assertEqual(
            self.tageschauScraper.is_url_valid("https://www.tagesschau.de/archiv/?datum=2022-01-01&ressort=wirtschaft"),
            True
            )
        
    # def test_get_all_news_teaser(self):
    #     response = requests.get(self.url)
    #     soup = get_soup(response)
    #     all_news_teaser = self.tageschauScraper.get_all_news_teaser(soup)
    #     self.assertEqual(all_news_teaser, self.test_teasers)

        
if __name__ == '__main__':
    unittest.main()