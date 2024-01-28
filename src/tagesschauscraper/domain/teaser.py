from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

from bs4 import BeautifulSoup, Tag

from tagesschauscraper.domain.helper import (
    AbstractScraper,
    Config,
    SoapValidator,
    TagDefinition,
    extract_text,
    HtmlTagNotExists,
    extract_link,
    get_extraction_timestamp,
)


@dataclass
class Teaser:
    date: str
    topline: str
    headline: str
    shorttext: str
    article_link: str
    extraction_timestamp: str


class TeaserScraper(AbstractScraper):
    """
    A class for extracting information from news teaser elements.
    """

    def __init__(self, soup: BeautifulSoup, config: Config) -> None:
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
            soup=self.soup,
            validation_config=self.config.validation,
        )
        validator.validate()
        return validator.valid

    def extract_tag(
        self, tag: TagDefinition, extract_function: Callable = extract_text
    ) -> str:
        page_elements = self.soup.find_all(name=tag.name, attrs=tag.attrs)
        if page_elements:
            extracted_content = [
                extract_function(page_element)
                for page_element in page_elements
                if isinstance(page_element, Tag)
            ]
            return self.concatenate_extracted_content(extracted_content)
        raise HtmlTagNotExists(
            f"No element found in html with name {tag.name} and attrs"
            f" {tag.attrs}"
        )

    def concatenate_extracted_content(
        self, content: List[str], delimiter="|"
    ) -> str:
        return delimiter.join(content)

    def extract(self) -> Teaser:
        tags = self.config.scraping
        teaser = Teaser(
            date=self.extract_tag(tags["date"], extract_text),
            topline=self.extract_tag(tags["topline"], extract_text),
            headline=self.extract_tag(tags["headline"], extract_text),
            shorttext=self.extract_tag(tags["shorttext"], extract_text),
            article_link=self.extract_tag(tags["article_link"], extract_link),
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
