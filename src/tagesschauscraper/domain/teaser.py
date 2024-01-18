from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Callable, Dict

from bs4 import BeautifulSoup, Tag

from tagesschauscraper.domain.helper import (
    AbstractScraper,
    TagDefinition,
    extract_link,
    extract_text,
    is_tag_in_soup,
    get_extraction_timestamp,
)


class HtmlTagNotExists(Exception):
    pass


@dataclass
class RequiredContent:
    tag_definition: TagDefinition


class SoapValidator:
    def __init__(self, soup: BeautifulSoup, required_content: RequiredContent):
        self.soup = soup
        self.required_content = required_content
        self.valid = False

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
            self.soup, self.required_content.tag_definition
        )


@dataclass
class Teaser:
    date: str
    topline: str
    headline: str
    shorttext: str
    article_link: str
    extraction_timestamp: str


@dataclass
class TeaserConfig:
    required: TagDefinition
    tags: Dict[str, TagDefinition]


class TeaserScraper(AbstractScraper):
    """
    A class for extracting information from news teaser elements.
    """

    def __init__(self, soup: BeautifulSoup, config: TeaserConfig) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup
        self.config = config

    def can_scrape(self) -> Optional[bool]:
        validator = SoapValidator(
            self.soup,
            required_content=RequiredContent(
                # tag_definition=TagDefinition(**self.config.required)
                tag_definition=self.config.required
            ),
        )
        validator.validate()
        return validator.valid

    def extract_tag(
        self, tag: TagDefinition, extract_function: Callable = extract_text
    ) -> str:
        page_elements = self.soup.find_all(name=tag.name, attrs=tag.attrs)
        if page_elements:
            links: List = []
            for page_element in page_elements:
                if isinstance(page_element, Tag):
                    link = extract_function(page_element)
                    links.append(link)
            return "|".join(links)
        raise HtmlTagNotExists(
            f"No element found in html with name {tag.name} and attrs"
            f" {tag.attrs}"
        )

    def extract_article_link(self) -> str:
        # tag = TagDefinition(**self.config.tags["article_link"])
        tag = self.config.tags["article_link"]
        return self.extract_tag(tag, extract_function=extract_link)

    def extract_topline(self) -> str:
        tag = TagDefinition(attrs={"class": "teaser-right__labeltopline"})
        return self.extract_tag(tag, extract_function=extract_text)

    def extract_headline(self) -> str:
        tag = self.soup.find(attrs={"class": "teaser-right__headline"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_shorttext(self) -> str:
        tag = self.soup.find(attrs={"class": "teaser-right__shorttext"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract_date(self) -> str:
        tag = self.soup.find(attrs={"class": "teaser-right__date"})
        if isinstance(tag, Tag):
            return extract_text(tag)

    def extract(self) -> Teaser:
        teaser = Teaser(
            date=self.extract_date(),
            topline=self.extract_topline(),
            headline=self.extract_headline(),
            shorttext=self.extract_shorttext(),
            article_link=self.extract_article_link(),
            extraction_timestamp=get_extraction_timestamp(),
        )
        return teaser


def scrape_teaser_list(teaser_list: List[str]) -> List[Teaser]:
    """
    Domain service function for retrieving a list of teasers
    """
    result = []
    for raw_teaser in teaser_list:
        scraper = TeaserScraper(raw_teaser)
        teaser = scraper.extract()
        result.append(teaser)
    return result
