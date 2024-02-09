from __future__ import annotations

from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from bluescraper.config import Config, TagScrapingConfig
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
        self,
        soup: BeautifulSoup,
        tag: TagDefinition,
        content_type: Optional[str],
    ) -> str:
        page_elements = soup.find_all(name=tag.name, attrs=tag.attrs)
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
        if self.config.scraping.groups:
            for group in self.config.scraping.groups:
                soup_batches = self.soup.find_all(
                    name=group.tag.name, attrs=group.tag.attrs
                )
                result = {
                    group.id: [
                        {
                            tag.id: self.extract_tag(
                                soup=soup,
                                tag=tag.tag,
                                content_type=tag.content_type,
                            )
                            for tag in get_group_tags(
                                group.contains, self.config.scraping.tags
                            )
                        }
                        for soup in soup_batches
                    ]
                }
        else:
            tags = self.config.scraping.tags
            result = {
                tag.id: self.extract_tag(
                    tag=tag.tag,
                    content_type=tag.content_type,
                )
                for tag in tags
            }
        return result


def get_group_tags(
    contains: List[str], tags: List[TagScrapingConfig]
) -> List[TagScrapingConfig]:
    return [tag for tag in tags if tag.id in contains]
