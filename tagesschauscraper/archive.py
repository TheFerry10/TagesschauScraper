from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Union

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from tagesschauscraper import constants
from tagesschauscraper.constants import (
    ARCHIVE_URL,
    DEFAULT_DATE_PATTERN,
    DEFAULT_TIMEOUT,
    NEWS_CATEGORIES,
)
from tagesschauscraper.helper import (
    AbstractContent,
    TagDefinition,
    is_tag_in_soup,
    is_text_in_tag,
)


@dataclass(frozen=True)
class ArchiveFilter:
    date: date
    news_category: str | None


def transform_date(date_: date, date_pattern: str = DEFAULT_DATE_PATTERN) -> str:
    return date_.strftime(date_pattern)


def transform_date_to_date_in_headline(date_: date) -> str:
    year = date_.year
    month = date_.month
    day = date_.day
    return f"{day}. {constants.german_month_names[month]} {year}"


def transform_date_in_headline_to_date(date_in_headline: str) -> date:
    day_raw, month_raw, year_raw = date_in_headline.split()
    day = int(day_raw[:-1])
    month = constants.german_month_names.index(month_raw)
    year = int(year_raw)
    return date(year, month, day)


def is_selected_in_categories(
    category: str,
) -> bool:
    return category in NEWS_CATEGORIES


class Archive(AbstractContent):
    """
    A class for extracting information from news archive.
    """

    RequiredHTMLContent = {
        "tagDefinition": TagDefinition("div", {"class": "trenner__text__topline"}),
        "text": "Archiv",
    }

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Archive with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup
        self.valid = False
        self.validate()

    def validate(self) -> None:
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
        ) & is_text_in_tag(
            self.soup,
            self.RequiredHTMLContent["tagDefinition"],
            self.RequiredHTMLContent["text"],
        )

    def extract(self) -> None:
        pass

    def extract_teaser_list(self):
        teaser_container = self.soup.find_all("div", {"class": "teaser-right twelve"})
        return teaser_container

    def extract_news_categories(self) -> set:
        category_container = self.soup.find("ul", {"class": "tabnav__list swipe"})
        categories: set[str] = set()
        if isinstance(category_container, Tag):
            categories = {
                category_element.get_text(strip=True)
                for category_element in category_container.find_all(
                    "li", {"class": "tabnav__item"}
                )
            }
        return categories

    def extract_date(self):
        date_tag = self.soup.find(attrs={"class": "archive__headline"})
        if date_tag:
            return date_tag.get_text(strip=True)


def is_category_valid(category: str | None) -> bool:
    return (category in NEWS_CATEGORIES) | (category is None)


def create_request_params(archive_filter: ArchiveFilter) -> dict:
    if is_category_valid(archive_filter.news_category):
        return {
            "datum": transform_date(archive_filter.date),
            "filter": archive_filter.news_category,
        }
    else:
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
    response = requests.get(ARCHIVE_URL, params=request_params, timeout=DEFAULT_TIMEOUT)
    if response.ok:
        return response
    else:
        return None


def get_archive_html(archive_filter: ArchiveFilter) -> BeautifulSoup:
    request_params = create_request_params(archive_filter)
    response = requests.get(ARCHIVE_URL, params=request_params)
    return BeautifulSoup(response.text, "html.parser")
