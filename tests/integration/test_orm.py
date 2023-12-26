from sqlalchemy.sql import text
from tagesschauscraper.domain.article import Article
from tagesschauscraper.domain.teaser import Teaser


def test_teaser_mapper_can_load_teasers(session):
    query = (
        "INSERT INTO teasers (date, shorttext, headline, topline, article_link, extraction_timestamp) VALUES "
        '("08.10.2023 • 13:17 Uhr", "Test short text", "Test headline", "Test topline", "/dummy/article.html", "2023-01-01T00:00:00"),'
        '("08.10.2023 • 15:17 Uhr", "Test short text 2", "Test headline 2", "Test topline 2", "/dummy/article_2.html", "2023-01-02T00:00:00")'
    )
    session.execute(text(query))

    expected = [
        Teaser(
            date="08.10.2023 • 13:17 Uhr",
            shorttext="Test short text",
            headline="Test headline",
            topline="Test topline",
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        ),
        Teaser(
            date="08.10.2023 • 15:17 Uhr",
            shorttext="Test short text 2",
            headline="Test headline 2",
            topline="Test topline 2",
            article_link="/dummy/article_2.html",
            extraction_timestamp="2023-01-02T00:00:00",
        ),
    ]
    assert session.query(Teaser).all() == expected


def test_teaser_mapper_can_save_teasers(session):
    new_teaser = Teaser(
        date="08.10.2023 • 13:17 Uhr",
        shorttext="Test short text",
        headline="Test headline",
        topline="Test topline",
        article_link="/dummy/article.html",
        extraction_timestamp="2023-01-01T00:00:00",
    )
    session.add(new_teaser)
    session.commit()
    query = 'SELECT date, shorttext, headline, topline, article_link, extraction_timestamp FROM "teasers"'
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


def test_retrieving_articles(session):
    query = (
        "INSERT INTO articles (abstract, topline, headline, metatextline, paragraphs, subheads, tags, article_link, extraction_timestamp) VALUES "
        '("Test abstract", "Test topline", "Test headline", "Stand: 07.10.2023 17:43 Uhr", "Paragraph 1", "Subhead 1|Subhead 2", "tag1|tag2|tag3", "/dummy/article.html", "2023-01-01T00:00:00"),'
        '("Test abstract 2", "Test topline 2", "Test headline 2", "Stand: 07.11.2023 17:43 Uhr", "Paragraph 2", "Subhead 1|Subhead 3", "tag1|tag2|tag4", "/dummy/article_2.html", "2023-01-02T00:00:00")'
    )
    session.execute(text(query))
    expected = [
        Article(
            abstract="Test abstract",
            topline="Test topline",
            headline="Test headline",
            metatextline="Stand: 07.10.2023 17:43 Uhr",
            paragraphs="Paragraph 1",
            subheads="Subhead 1|Subhead 2",
            tags="tag1|tag2|tag3",
            article_link="/dummy/article.html",
            extraction_timestamp="2023-01-01T00:00:00",
        ),
        Article(
            abstract="Test abstract 2",
            topline="Test topline 2",
            headline="Test headline 2",
            metatextline="Stand: 07.11.2023 17:43 Uhr",
            paragraphs="Paragraph 2",
            subheads="Subhead 1|Subhead 3",
            tags="tag1|tag2|tag4",
            article_link="/dummy/article_2.html",
            extraction_timestamp="2023-01-02T00:00:00",
        ),
    ]
    assert session.query(Article).all() == expected


def test_saving_articles(session):
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
    session.add(new_article)
    session.commit()
    query = "SELECT abstract, topline, headline, metatextline, paragraphs, subheads, tags, article_link, extraction_timestamp FROM 'articles'"
    rows = list(session.execute(text(query)))
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
