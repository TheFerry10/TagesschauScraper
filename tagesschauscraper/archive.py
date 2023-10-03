from __future__ import annotations
from datetime import date
from dataclasses import dataclass
from bs4 import BeautifulSoup
from bs4.element import Tag
from tagesschauscraper import constants
from tagesschauscraper.helper import (
    AbstractContent,
    TagDefinition,
    is_tag_in_soup,
    is_text_in_tag,
)


ARCHIVE_URL = "https://www.tagesschau.de/archiv/"
NEWS_CATEGORIES = ["wirtschaft", "inland", "ausland"]
DEFAULT_DATE_PATTERN = "%Y-%m-%d"


@dataclass(frozen=True)
class ArchiveFilter:
    date: date
    news_category: str


def transform_date(
    date_: date, date_pattern: str = DEFAULT_DATE_PATTERN
) -> str:
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
        "tagDefinition": TagDefinition(
            "div", {"class": "trenner__text__topline"}
        ),
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
        self.valid = is_tag_in_soup(
            self.soup, Archive.RequiredHTMLContent["tagDefinition"]
        ) & is_text_in_tag(
            self.soup,
            Archive.RequiredHTMLContent["tagDefinition"],
            Archive.RequiredHTMLContent["text"],
        )

    def extract(self) -> None:
        pass

    def extract_teaser_list(self):
        teaser_container = self.soup.find_all(
            "div", {"class": "teaser-right twelve"}
        )
        return teaser_container

    def extract_news_categories(self) -> set:
        category_container = self.soup.find(
            "ul", {"class": "tabnav__list swipe"}
        )
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


def create_request_params(archive_filter: ArchiveFilter) -> dict:
    return {
        "datum": transform_date(archive_filter.date),
        "filter": archive_filter.news_category,
    }
