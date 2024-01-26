import os
from pathlib import Path

from sqlalchemy.sql import text

from tagesschauscraper.adapters import repository
from tagesschauscraper.domain.article import Article
from tagesschauscraper.domain.teaser import Teaser


def test_repository_can_save_a_teaser(session):
    new_teaser = Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    repo = repository.SqlAlchemyTeaserRepository(session)
    repo.add(new_teaser)
    session.commit()
    query = (
        "SELECT date, shorttext, headline, topline, article_link,"
        ' extraction_timestamp FROM "teasers"'
    )
    rows = list(session.execute((text(query))))
    assert rows == [
        (
            "08.10.2023 • 13:17 Uhr",
            "Test short text",
            "Test headline",
            "Test topline",
            "/dummy/article.html",
            "2023-01-01T00:00:00",
        )
    ]


def test_repository_can_save_an_article(session):
    new_article = Article(
        abstract="Test abstract",
        topline="Test topline",
        headline="Test headline",
        metatextline="Stand: 07.10.2023 17:43 Uhr",
        paragraphs="Paragraph 1",
        subheads="Subhead 1|Subhead 2",
        tags="tag1|tag2|tag3",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    repo = repository.SqlAlchemyArticleRepository(session)
    repo.add(new_article)
    session.commit()
    query = (
        "SELECT abstract, topline, headline, metatextline, paragraphs,"
        " subheads, tags, article_link, extraction_timestamp FROM 'articles'"
    )
    rows = list(session.execute((text(query))))
    assert rows == [
        (
            "Test abstract",
            "Test topline",
            "Test headline",
            "Stand: 07.10.2023 17:43 Uhr",
            "Paragraph 1",
            "Subhead 1|Subhead 2",
            "tag1|tag2|tag3",
            "/dummy/article.html",
            "2023-01-01T00:00:00",
        )
    ]


def test_csv_repository_can_add_a_teaser():
    """
    Not testing that the teaser is added to the csv!!
    """
    new_teaser = Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    test_folder = Path("./tests/data/teaser")
    repo = repository.CsvTeaserRepository(test_folder)
    repo.add(new_teaser)
    rows = repo.list()

    assert rows == [new_teaser]
