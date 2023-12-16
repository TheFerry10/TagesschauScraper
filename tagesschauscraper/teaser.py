from __future__ import annotations

import csv
import os
from datetime import date, datetime
from typing import Sequence, Union

from bs4 import BeautifulSoup, Tag

from tagesschauscraper.helper import (
    AbstractContent,
    TagDefinition,
    extract_link,
    extract_text,
    is_tag_in_soup,
)


class Teaser(AbstractContent):
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

    def get_extraction_timestamp(self) -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat()

    def extract(self):
        """
        Extracts structured information from a teaser.
        The extracted elements are:
        * date
        * topline
        * headline
        * shorttext
        * article link

        Returns
        -------
        dict
            A dictionary containing all the information of the news teaser
        """
        field_extraction_function_pairs = {
            "DATE": self.extract_date,
            "TOPLINE": self.extract_topline,
            "HEADLINE": self.extract_headline,
            "SHORTTEXT": self.extract_shorttext,
            "ARTICLE_LINK": self.extract_article_link,
            "EXTRACTION_TIMESTAMP": self.get_extraction_timestamp,
        }
        return {
            field: extraction_function()
            for field, extraction_function in field_extraction_function_pairs.items()
        }


def write_teaser_list(teaser_list: Sequence[dict]):
    datetime_str = datetime.utcnow().replace(microsecond=0).strftime("%Y%m%d%H%M")
    output_dir = "data"
    file_name = f"teaser_{datetime_str}.csv"
    with open(os.path.join(output_dir, file_name), "w", newline="") as csvfile:
        fieldnames = [
            "DATE",
            "TOPLINE",
            "HEADLINE",
            "SHORTTEXT",
            "ARTICLE_LINK",
            "EXTRACTION_TIMESTAMP",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teaser_list)
