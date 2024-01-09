import pytest
from sqlalchemy.sql import text

from tagesschauscraper.service_layer import unit_of_work


def insert_teaser(
    session,
    date,
    shorttext,
    headline,
    topline,
    article_link,
    extraction_timestamp,
):
    session.execute(
        text(
            "INSERT INTO teasers (date, shorttext, headline, topline,"
            " article_link, extraction_timestamp) VALUES (:date, :shorttext,"
            " :headline, :topline, :article_link, :extraction_timestamp)"
        ),
        dict(
            date=date,
            shorttext=shorttext,
            headline=headline,
            topline=topline,
            article_link=article_link,
            extraction_timestamp=extraction_timestamp,
        ),
    )


def get_teaser_article_link(session, article_link):
    [[batchref]] = session.execute(
        text(
            "SELECT article_link FROM teasers WHERE article_link=:article_link"
        ),
        dict(article_link=article_link),
    )
    return batchref


def test_uow_can_retrieve_a_teaser(session_factory):
    session = session_factory()
    insert_teaser(
        session,
        "08.10.2023 • 13:17 Uhr",
        "Test short text",
        "Test headline",
        "Test topline",
        "/dummy/article.html",
        "2023-01-01T00:00:00",
    )
    session.commit()
    article_link = "/dummy/article.html"
    uow = unit_of_work.SqlAlchemyTeaserUnitOfWork(session_factory)
    with uow:
        teaser = uow.teasers.get(article_link=article_link)
        uow.commit()

    article_link_ = get_teaser_article_link(session, article_link)
    assert article_link_ == article_link
