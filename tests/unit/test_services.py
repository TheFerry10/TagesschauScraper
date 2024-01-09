import datetime
from pathlib import Path
from unittest.mock import patch

from tagesschauscraper.domain.archive import ArchiveFilter
from tagesschauscraper.domain.article import Article
from tagesschauscraper.domain.teaser import Teaser
from tagesschauscraper.service_layer.service import (
    scrape_article,
    scrape_teaser,
)

ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")


@patch("tagesschauscraper.domain.archive.requests.get")
def test_scrape_all_teaser_for_date(mock_get, archive_with_teaser_list_html):
    mock_get.return_value.ok = True
    mock_get.return_value.text = archive_with_teaser_list_html
    expected_teaser_list = [
        Teaser(
            date="08.10.2023 • 13:17 Uhr",
            shorttext="Test short text",
            headline="Test headline",
            topline="Test topline",
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        )
    ]

    archive_filter = ArchiveFilter(
        date=datetime.date(2023, 11, 4), news_category="wirtschaft"
    )
    teaser_list = scrape_teaser(
        archive_filter, extraction_timestamp=datetime.datetime(2023, 1, 1)
    )
    assert expected_teaser_list == teaser_list


@patch("tagesschauscraper.domain.article.requests.get")
def test_scrape_articles_from_teaser(mock_get, expected_article_html):
    mock_get.return_value.ok = True
    mock_get.return_value.text = expected_article_html
    expected_article_list = [
        Article(
            abstract="Test abstract",
            topline="Test topline",
            headline="Test headline",
            metatextline="Stand: 07.10.2023 17:43 Uhr",
            paragraphs="|".join(["Paragraph 1"]),
            subheads="|".join(["Subhead 1", "Subhead 2"]),
            tags="|".join(["tag1", "tag2", "tag3"]),
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        )
    ]
    teaser_list = [
        Teaser(
            date="08.10.2023 • 13:17 Uhr",
            shorttext="Test short text",
            headline="Test headline",
            topline="Test topline",
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        )
    ]
    article_list = scrape_article(
        teaser_list, extraction_timestamp=datetime.datetime(2023, 1, 1)
    )
    assert article_list == expected_article_list
