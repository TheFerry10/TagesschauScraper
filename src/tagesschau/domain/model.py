from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from bluescraper.constants import DEFAULT_TIMEOUT
from bluescraper.utils import TagDefinition, transform_date
from tagesschau.domain.constants import (
    ARCHIVE_URL,
    NEWS_CATEGORIES,
    TAGESSCHAU_URL,
)


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


def is_selected_in_categories(
    category: str,
) -> bool:
    return category in NEWS_CATEGORIES


def extract_teaser_list(soup: BeautifulSoup) -> List[Tag]:
    teaser_tag = TagDefinition(
        name="div", attrs={"class": "teaser-right twelve"}
    )
    teaser_container = soup.find_all(
        name=teaser_tag.name, attrs=teaser_tag.attrs
    )
    return teaser_container


def is_category_valid(category: str | None) -> bool:
    return (category in NEWS_CATEGORIES) | (category is None)


def create_request_params(archive_filter: ArchiveFilter) -> dict:
    if is_category_valid(archive_filter.news_category):
        return {
            "datum": transform_date(archive_filter.date),
            "filter": archive_filter.news_category,
        }
    raise ValueError


def get_archive_response(request_params: dict) -> Union[Response, None]:
    """
    Service for retrieving the html of the archive.

    Parameters
    ----------
    request_params : dict
        HTTP request params

    Returns
    -------
    str
        HTML of archive
    """
    response = requests.get(
        ARCHIVE_URL, params=request_params, timeout=DEFAULT_TIMEOUT
    )
    if response.ok:
        return response
    else:
        return None


def get_archive_html(archive_filter: ArchiveFilter) -> BeautifulSoup:
    request_params = create_request_params(archive_filter)
    response = requests.get(
        ARCHIVE_URL, params=request_params, timeout=DEFAULT_TIMEOUT
    )
    return BeautifulSoup(response.text, "html.parser")


class ArticleTagNotFound(Exception):
    pass


def get_article_response(link: str) -> Union[Response, None]:
    """
    Service for retrieving the html of the article.

    Parameters
    ----------
    request_params : dict
        HTTP request params

    Returns
    -------
    str
        HTML of archive
    """
    url = urljoin(TAGESSCHAU_URL, link)
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    if response.ok:
        return response
    else:
        return None


def get_article_html(link: str) -> BeautifulSoup:
    response = get_article_response(link)
    return BeautifulSoup(response.text, "html.parser")


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
