import json
import unittest
from datetime import date

from bs4 import BeautifulSoup

from tagesschauscraper.tagesschau import (
    Archive,
    Article,
    TagesschauScraper,
    Teaser,
    create_url_for_news_archive,
)


class TestTagesschauScraper(unittest.TestCase):
    def setUp(self):
        with open("tests/data/archive.html", "r") as f:
            markup = f.read()
        self.soup = BeautifulSoup(markup, "html.parser")
        self.tageschauScraper = TagesschauScraper()

    def test___extract_info_for_all_teaser(self):
        all_teaser = self.tageschauScraper._extract_info_for_all_teaser(
            self.soup
        )
        with open("tests/data/all_teaser.json", "r") as f:
            true_all_teaser = json.load(f)
        self.assertDictEqual(all_teaser, true_all_teaser)

    def test_scrape_teaser(self):
        url = "https://www.tagesschau.de/archiv/?datum=2022-03-01&ressort=wirtschaft"
        all_teaser = self.tageschauScraper.scrape_teaser(url)
        with open("tests/data/all_teaser.json", "r") as f:
            true_all_teaser = json.load(f)
        self.assertDictEqual(all_teaser, true_all_teaser)


class TestTeaser(unittest.TestCase):
    def setUp(self):
        with open("tests/data/teaser.html", "r") as f:
            markup = f.read()
        self.soup = BeautifulSoup(markup, "html.parser")
        self.teaser = Teaser(self.soup)

    def test_extract_info_from_teaser(self):
        teaser_info = self.teaser.extract_info_from_teaser()
        true_teaser_info = {
            "date": "01.03.2022 - 18:54 Uhr",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
        }
        self.assertDictEqual(teaser_info, true_teaser_info)

    def test_enrich_teaser_info_with_article_tags(self):
        teaser_info = {
            "date": "01.03.2022 - 18:54 Uhr",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
        }

        true_enriched_teaser_info = {
            "date": "01.03.2022 - 18:54 Uhr",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            "tags": ",".join(
                sorted(
                    [
                        "Nord Stream 2",
                        "Insolvenz",
                        "Schweiz",
                        "Pipeline",
                        "Russland",
                    ]
                )
            ),
        }

        enriched_teaser_info = (
            self.teaser.enrich_teaser_info_with_article_tags(teaser_info)
        )
        self.assertDictEqual(enriched_teaser_info, true_enriched_teaser_info)

    def test_process_info(self):
        teaser_info = {
            "date": "01.03.2022 - 18:54 Uhr",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            "tags": ",".join(
                sorted(
                    [
                        "Nord Stream 2",
                        "Insolvenz",
                        "Schweiz",
                        "Pipeline",
                        "Russland",
                    ]
                )
            ),
        }

        true_processed_teaser_info = {
            "id": "595aa643ed39edd3695b8401a99ce808afa539fb",
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            "tags": ",".join(
                sorted(
                    [
                        "Nord Stream 2",
                        "Insolvenz",
                        "Schweiz",
                        "Pipeline",
                        "Russland",
                    ]
                )
            ),
        }

        processed_teaser_info = self.teaser.process_info(teaser_info)
        self.assertDictEqual(processed_teaser_info, true_processed_teaser_info)

    def test_is_teaser_info_valid_complete(self):
        teaser_info = {
            "id": "595aa643ed39edd3695b8401a99ce808afa539fb",
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            "tags": ",".join(
                sorted(
                    [
                        "Nord Stream 2",
                        "Insolvenz",
                        "Schweiz",
                        "Pipeline",
                        "Russland",
                    ]
                )
            ),
        }
        self.assertEqual(self.teaser.is_teaser_info_valid(teaser_info), True)

    def test_is_teaser_info_valid_no_link(self):
        teaser_info = {
            "id": "595aa643ed39edd3695b8401a99ce808afa539fb",
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "tags": ",".join(
                sorted(
                    [
                        "Nord Stream 2",
                        "Insolvenz",
                        "Schweiz",
                        "Pipeline",
                        "Russland",
                    ]
                )
            ),
        }
        self.assertEqual(self.teaser.is_teaser_info_valid(teaser_info), False)


class TestArticle(unittest.TestCase):
    def setUp(self):
        with open("tests/data/article.html", "r") as f:
            markup = f.read()
        self.soup = BeautifulSoup(markup, "html.parser")

    def test_extract_article_tags(self):
        article = Article(self.soup)
        article_tags = article.extract_article_tags()
        true_article_tags = {
            "tags": ",".join(
                sorted(["Marktbericht", "Börse", "DAX", "Dow Jones"])
            )
        }
        self.assertDictEqual(article_tags, true_article_tags)


class TestArchive(unittest.TestCase):
    def setUp(self):
        with open("tests/data/archive.html", "r") as f:
            markup = f.read()
        self.soup = BeautifulSoup(markup, "html.parser")

    def test_transform_date_to_date_in_headline(self):
        date_ = date(2022, 3, 1)
        true_date_in_headline = "1. März 2022"
        archive = Archive(self.soup)
        date_in_headline = archive.transform_date_to_date_in_headline(date_)
        self.assertEqual(date_in_headline, true_date_in_headline)

    def test_transform_date_in_headline_to_date(self):
        date_in_headline = "1. März 2022"
        true_date = date(2022, 3, 1)
        archive = Archive(self.soup)
        date_ = archive.transform_date_in_headline_to_date(date_in_headline)
        self.assertEqual(date_, true_date)

    def test_extract_info_from_archive(self):
        archive = Archive(self.soup)
        archive_info = archive.extract_info_from_archive()
        true_archive_info = {"headline": "1. März 2022", "num_teaser": "20"}
        self.assertEqual(archive_info, true_archive_info)


class TestCreateURL(unittest.TestCase):
    def test_create_url_for_news_archive(self):
        urls = {
            "wirtschaft": "https://www.tagesschau.de/archiv/?datum=2022-03-01&ressort=wirtschaft",
            "inland": "https://www.tagesschau.de/archiv/?datum=2022-03-01&ressort=inland",
            "ausland": "https://www.tagesschau.de/archiv/?datum=2022-03-01&ressort=ausland",
            "all": "https://www.tagesschau.de/archiv/?datum=2022-03-01",
        }
        date_ = date(2022, 3, 1)
        self.assertEqual(
            create_url_for_news_archive(date_=date_, category="wirtschaft"),
            urls["wirtschaft"],
        )
        self.assertEqual(
            create_url_for_news_archive(date_=date_, category="inland"),
            urls["inland"],
        )
        self.assertEqual(
            create_url_for_news_archive(date_=date_, category="ausland"),
            urls["ausland"],
        )
        self.assertEqual(
            create_url_for_news_archive(date_=date_, category="all"),
            urls["all"],
        )


if __name__ == "__main__":
    unittest.main()
