from __future__ import annotations

from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from bluescraper.config import Config
from bluescraper.utils import TagDefinition, extract_from_tag
from bluescraper.validation import SoapValidator


class HtmlTagNotExists(Exception):
    pass


class NotValidHTML(Exception):
    pass


class Scraper:
    """
    A class for extracting information from beautifulsoup.
    """

    def __init__(self, soup: BeautifulSoup, config: Config) -> None:
        self.soup = soup
        self.config = config

    def can_scrape(self) -> bool:
        if self.config.validation:
            validator = SoapValidator(
                soup=self.soup,
                validation_config=self.config.validation,
            )
            validator.validate()
            return validator.valid
        return True

    def extract_tag(
        self, tag: TagDefinition, content_type: Optional[str]
    ) -> str:
        page_elements = self.soup.find_all(name=tag.name, attrs=tag.attrs)
        if page_elements:
            extracted_content = [
                extract_from_tag(tag=page_element, key=content_type)
                for page_element in page_elements
                if isinstance(page_element, Tag)
            ]
            return self.concatenate_extracted_content(extracted_content)
        raise HtmlTagNotExists(
            f"No element found in html with name {tag.name} and attrs"
            f" {tag.attrs}"
        )

    def concatenate_extracted_content(
        self, content: Optional[List[str]], delimiter="|"
    ) -> Optional[str]:
        if content:
            return delimiter.join(content)
        return None

    def extract(self) -> dict:
        # extraction_timestamp=get_extraction_timestamp(),
        # extract_function = {"text": extract_text, "href": extract_link, "content"}
        # extract_from_tag()
        tags = self.config.scraping.tags
        return {
            tag.id: self.extract_tag(
                tag=tag.tag,
                content_type=tag.content_type,
            )
            for tag in tags
        }
