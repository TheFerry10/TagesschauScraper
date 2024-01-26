from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List, Optional, Union
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

from tagesschauscraper.domain.constants import DEFAULT_TIMEOUT, TAGESSCHAU_URL
from tagesschauscraper.domain.helper import (
    AbstractScraper,
    TagDefinition,
    extract_text,
    get_extraction_timestamp,
    is_tag_in_soup,
)
from tagesschauscraper.domain.teaser import Teaser


@dataclass(frozen=False)
class Article:
    topline: str
    headline: str
    metatextline: str
    tags: str
    subheads: str
    abstract: str
    paragraphs: str
    article_link: str
    extraction_timestamp: str


class ArticleTagNotFound(Exception):
    pass


class ArticleScraper(AbstractScraper):
    """
    A class for extracting information from news article HTML elements.
    """

    RequiredHTMLContent = {
        "tagDefinition": TagDefinition("div", {"class": "seitenkopf__title"}),
    }

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup
        self.valid = False
        self.validate()

    def validate(self):
        """
        Check if scraped information exists for all required attributes.

        Parameters
        ----------
        teaser_info : dict
            Dictionary containing news teaser information.

        Returns
        -------
        bool
            News teaser information is valid, when the function returns True.
        """
        self.valid = is_tag_in_soup(
            self.soup, self.RequiredHTMLContent["tagDefinition"]
        )

    def extract(self) -> Article:
        return Article(
            topline=self.extract_topline(),
            headline=self.extract_headline(),
            metatextline=self.extract_metatextline(),
            tags=self.extract_tags(),
            subheads=self.extract_subheads(),
            abstract=self.extract_abstract(),
            paragraphs=self.extract_paragraphs(),
            article_link="",
            extraction_timestamp=get_extraction_timestamp(),
        )

    def extract_topline(self):
        tag = self.soup.find(attrs={"class": "seitenkopf__topline"})
        if isinstance(tag, Tag):
            return extract_text(tag)
        else:
            raise ArticleTagNotFound(
                "Topline not found for class: seitenkopf__topline"
            )

    def extract_headline(self):
        tag = self.soup.find(attrs={"class": "seitenkopf__headline--text"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_metatextline(self):
        tag = self.soup.find(attrs={"class": "metatextline"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_tags(self):
        tag = self.soup.find(attrs={"class": "taglist"})
        article_tags = tag.find_all("li", {"class": "taglist__element"})
        return "|".join(
            [extract_text(tag) for tag in article_tags if isinstance(tag, Tag)]
        )

    def extract_subheads(self):
        tags = self.soup.find_all(
            attrs={
                "class": (
                    "meldung__subhead columns twelve m-ten m-offset-one"
                    " l-eight l-offset-two liveblog--anchor"
                )
            }
        )
        return "|".join(
            [extract_text(tag) for tag in tags if isinstance(tag, Tag)]
        )

    def extract_abstract(self):
        tag = self.soup.find(
            attrs={
                "class": (
                    "textabsatz columns twelve m-ten m-offset-one l-eight"
                    " l-offset-two"
                )
            }
        )
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_paragraphs(self):
        tags = self.soup.find_all(
            attrs={
                "class": (
                    "textabsatz m-ten m-offset-one l-eight l-offset-two"
                    " columns twelve"
                )
            }
        )
        return "|".join(
            [extract_text(tag) for tag in tags if isinstance(tag, Tag)]
        )


def get_article_html(link: str) -> BeautifulSoup:
    response = get_article_response(link)
    return BeautifulSoup(response.text, "html.parser")


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


def scrape_article(teaser_list: List[Teaser]) -> List[Article]:
    article_list: List[Article] = []
    for t in teaser_list:
        raw_article = get_article_html(t.article_link)
        article = ArticleScraper(raw_article).extract()
        article.article_link = t.article_link
        article_list.append(article)
    return article_list
