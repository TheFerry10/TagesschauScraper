from __future__ import annotations

import csv
import datetime
import os
from dataclasses import dataclass
from typing import Sequence, Union

from bs4 import BeautifulSoup, Tag

from tagesschauscraper.domain.helper import (
    AbstractScraper,
    TagDefinition,
    extract_link,
    extract_text,
    is_tag_in_soup,
)


@dataclass
class Teaser:
    date: str
    topline: str
    headline: str
    shorttext: str
    article_link: str
    extraction_timestamp: str | None = None


class TeaserScraper(AbstractScraper):
    """
    A class for extracting information from news teaser elements.
    """

    RequiredHTMLContent = {
        "tagDefinition": TagDefinition("div", {"class": "teaser-right twelve"}),
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

    def extract_article_link(self) -> Union[str, None]:
        tag = self.soup.find(attrs={"class": "teaser-right__link"})
        if isinstance(tag, Tag):
            return extract_link(tag)

    def extract_topline(self) -> Union[str, None]:
        tag = self.soup.find(attrs={"class": "teaser-right__labeltopline"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_headline(self) -> Union[str, None]:
        tag = self.soup.find(attrs={"class": "teaser-right__headline"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_shorttext(self) -> Union[str, None]:
        tag = self.soup.find(attrs={"class": "teaser-right__shorttext"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_date(self) -> Union[str, None]:
        tag = self.soup.find(attrs={"class": "teaser-right__date"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract(self, extraction_timestamp: datetime.datetime | None = None) -> Teaser:
        teaser = Teaser(
            date=self.extract_date(),
            topline=self.extract_topline(),
            headline=self.extract_headline(),
            shorttext=self.extract_shorttext(),
            article_link=self.extract_article_link(),
            extraction_timestamp=self.get_extraction_timestamp(extraction_timestamp),
        )
        return teaser


def write_teaser_list(teaser_list: Sequence[dict]):
    datetime_str = (
        datetime.datetime.utcnow().replace(microsecond=0).strftime("%Y%m%d%H%M")
    )
    output_dir = "data"
    file_name = f"teaser_{datetime_str}.csv"
    with open(
        os.path.join(output_dir, file_name), "w", newline="", encoding="utf8"
    ) as csv_file:
        fieldnames = [
            "DATE",
            "TOPLINE",
            "HEADLINE",
            "SHORTTEXT",
            "ARTICLE_LINK",
            "EXTRACTION_TIMESTAMP",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teaser_list)


def remove_extraction_timestamp(teaser: Teaser):
    """
    Remove the extraction timestamp from teaser

    Parameters
    ----------
    teaser : Teaser

    Returns
    -------
    Teaser
        Teaser with removed extraction timestamp
    """
    return setattr(teaser, "extraction_timestamp", None)
