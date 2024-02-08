from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from bluescraper.utils import TagDefinition
from tagesschau.domain.constants import ARCHIVE_URL, NEWS_CATEGORIES
from tagesschau.domain.utils import transform_date


@dataclass
class Archive:
    date: str
    news_category_names: str
    news_category_links: str


@dataclass
class Teaser:
    date: str
    topline: str
    headline: str
    shorttext: str
    article_link: str


@dataclass
class Article:
    topline: str
    headline: str
    metatextline: str
    tags: str
    subheads: str
    abstract: str
    paragraphs: str
    article_link: str


@dataclass
class ArchiveFilter:
    date: date
    news_category: Optional[str] = None


def extract_teaser_list(soup: BeautifulSoup) -> List[Tag]:
    teaser_definition = TagDefinition(
        name="div", attrs={"class": "teaser-right twelve"}
    )
    teaser_container = soup.find_all(
        name=teaser_definition.name, attrs=teaser_definition.attrs
    )
    return teaser_container


def is_category_valid(category: Optional[str]) -> bool:
    if isinstance(category, str):
        return category.lower() in NEWS_CATEGORIES
    return category is None


def create_request_params(archive_filter: ArchiveFilter) -> dict:
    if is_category_valid(archive_filter.news_category):
        return {
            "datum": transform_date(archive_filter.date),
            "filter": archive_filter.news_category,
        }
    raise ValueError


def get_archive_soup(archive_filter: ArchiveFilter) -> Optional[BeautifulSoup]:
    request_params = create_request_params(archive_filter)
    response = get_response(ARCHIVE_URL, request_params)
    if response:
        return BeautifulSoup(response.text, "html.parser")
    return None


class ArticleTagNotFound(Exception):
    pass


# def scrape_teaser_list(teaser_list: List[str]) -> List[Teaser]:
#     """
#     Domain service function for retrieving a list of teasers
#     """
#     result = []
#     for raw_teaser in teaser_list:
#         scraper = Scraper(raw_teaser)
#         teaser = scraper.extract()
#         result.append(teaser)
#     return result

# def scrape_article(teaser_list: List[Teaser]) -> List[Article]:
#     article_list: List[Article] = []
#     for t in teaser_list:
#         raw_article = get_article_html(t.article_link)
#         article = ArticleScraper(raw_article).extract()
#         article.article_link = t.article_link
#         article_list.append(article)
#     return article_list
