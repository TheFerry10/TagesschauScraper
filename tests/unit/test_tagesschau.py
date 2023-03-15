import unittest
from datetime import date
from bs4 import BeautifulSoup
from tagesschauscraper import tagesschau


class TestTagesschauScraper(unittest.TestCase):
    def setUp(self):
        with open("tests/data/teaser-list.html", "r") as f:
            html = f.read()
        self.soup = BeautifulSoup(html, "html.parser")
        self.tageschauScraper = tagesschau.TagesschauScraper()

    def test_extract_all_teaser(self):
        expected_teaser_list = {
            "records": [
                {
                    "date": "2022-03-01 22:23:00",
                    "topline": "Deutliche Verluste",
                    "headline": "Der Krieg lastet auf der Wall Street",
                    "shorttext": (
                        "Die intensiven Kämpfe in der Ukraine und die"
                        " Auswirkungen der Sanktionen verschreckten die"
                        " US-Investoren."
                    ),
                    "link": "https://www.tagesschau.de/wirtschaft/finanzen/marktberichte/marktbericht-dax-dow-jones-213.html",
                },
                {
                    "date": "2022-03-01 18:54:00",
                    "topline": "Pipeline-Projekt",
                    "headline": "Nordstream-Betreiber offenbar insolvent",
                    "shorttext": (
                        "Die Nord Stream 2 AG, die Schweizer"
                        " Eigentümergesellschaft der neuen Ostsee-Pipeline"
                        " nach Russland, ist offenbar insolvent."
                    ),
                    "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
                },
            ]
        }
        self.assertDictEqual(
            self.tageschauScraper._extract_all_teaser(self.soup),
            expected_teaser_list,
        )

    def test_enrich_teaser_info_with_article_tags(self):
        teaser_data = {
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

        true_enriched_teaser_data = {
            "id": "595aa643ed39edd3695b8401a99ce808afa539fb",
            "teaser": {
                "date": "01.03.2022 - 18:54 Uhr",
                "topline": "Pipeline-Projekt",
                "headline": "Nordstream-Betreiber offenbar insolvent",
                "shorttext": (
                    "Die Nord Stream 2 AG, die Schweizer"
                    " Eigentümergesellschaft der neuen Ostsee-Pipeline nach"
                    " Russland,\n                    ist offenbar insolvent."
                ),
                "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            },
            "article": {
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
            },
        }

        enriched_teaser_data = (
            self.tageschauScraper._merge_teaser_and_article_tags(teaser_data)
        )
        self.assertDictEqual(enriched_teaser_data, true_enriched_teaser_data)


class TestTeaser(unittest.TestCase):
    def setUp(self):
        with open("tests/data/teaser.html", "r") as f:
            html = f.read()
        self.soup = BeautifulSoup(html, "html.parser")
        self.teaser = tagesschau.Teaser(self.soup)

    def test_extract_info_from_teaser(self):
        teaser_info = self.teaser.extract_data_from_teaser()
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
        }

        true_processed_teaser_info = {
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
        }

        processed_teaser_info = self.teaser.process_extracted_data(teaser_info)
        self.assertDictEqual(processed_teaser_info, true_processed_teaser_info)

    def test_is_teaser_info_valid_complete(self):
        teaser_info = {
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
        }
        self.assertEqual(self.teaser.is_teaser_data_valid(teaser_info), True)

    def test_is_teaser_info_valid_no_link(self):
        teaser_info = {
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": (
                "Die Nord Stream 2 AG, die Schweizer Eigentümergesellschaft"
                " der neuen Ostsee-Pipeline nach Russland,\n                  "
                "  ist offenbar insolvent."
            ),
        }
        self.assertEqual(self.teaser.is_teaser_data_valid(teaser_info), False)


class TestArticle(unittest.TestCase):
    def setUp(self):
        with open("tests/data/article.html", "r") as f:
            html = f.read()
        self.soup = BeautifulSoup(html, "html.parser")
        self.article = tagesschau.Article(self.soup)

    def test_extract_article_tags(self):
        article_tags = self.article.extract_article_tags()
        expected_article_tags = {
            "tags": ",".join(
                sorted(["Marktbericht", "Börse", "DAX", "Dow Jones"])
            )
        }
        self.assertDictEqual(article_tags, expected_article_tags)


class TestArchive(unittest.TestCase):
    def setUp(self):
        with open("tests/data/archive.html", "r") as f:
            html = f.read()
        self.soup = BeautifulSoup(html, "html.parser")
        self.archive = tagesschau.Archive(self.soup)

    def test_extract_pagination(self):
        with open("tests/data/archive-pagination.html", "r") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        self.archive = tagesschau.Archive(soup)
        expected_pagination = [{"pageIndex": str(p)} for p in range(1, 4)]
        self.assertListEqual(
            self.archive.extract_pagination(), expected_pagination
        )

    def test_transform_date_to_date_in_headline(self):
        date_ = date(2022, 3, 1)
        true_date_in_headline = "1. März 2022"
        date_in_headline = self.archive.transform_date_to_date_in_headline(
            date_
        )
        self.assertEqual(date_in_headline, true_date_in_headline)

    def test_transform_date_in_headline_to_date(self):
        date_in_headline = "1. März 2022"
        true_date = date(2022, 3, 1)
        date_ = self.archive.transform_date_in_headline_to_date(
            date_in_headline
        )
        self.assertEqual(date_, true_date)

    def test_extract_info_from_archive(self):
        archive_info = self.archive.extract_info_from_archive()
        true_archive_info = {"headline": "1. März 2022", "num_teaser": "20"}
        self.assertEqual(archive_info, true_archive_info)


class TestArchiveFilter(unittest.TestCase):
    def test_input_processing(self):
        expected_parameter = {"datum": "2023-03-01", "ressort": "wirtschaft"}
        date_ = date(2023, 3, 1)
        category = "wirtschaft"
        raw_params = {"date": date_, "category": category}
        archiveFilter = tagesschau.ArchiveFilter(raw_params)
        self.assertDictEqual(
            archiveFilter.processed_params, expected_parameter
        )


if __name__ == "__main__":
    unittest.main()
