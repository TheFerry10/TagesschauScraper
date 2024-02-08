from sqlalchemy import Column, ForeignKey, MetaData, Table
from sqlalchemy.orm import registry, relationship
from sqlalchemy.types import Integer, String, Text

from tagesschau.domain.model import Article, Teaser

metadata = MetaData()
mapper_reg = registry()

teasers = Table(
    "teasers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", String(255)),
    Column("topline", String(255)),
    Column("headline", String(255)),
    Column("shorttext", Text()),
    Column("article_link", String(255)),
    Column("extraction_timestamp", String(255)),
)

articles = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("topline", String(255)),
    Column("headline", String(255)),
    Column("metatextline", String(255)),
    Column("tags", String(255)),
    Column("subheads", Text()),
    Column("abstract", Text()),
    Column("paragraphs", Text()),
    Column("article_link", ForeignKey("teasers.article_link")),
    Column("extraction_timestamp", String(255)),
)


def start_mappers():
    mapper_reg.map_imperatively(Teaser, teasers)
    mapper_reg.map_imperatively(
        Article, articles, properties={"teasers": relationship(Teaser)}
    )
