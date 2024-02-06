from typing import List, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel

from bluescraper.utils import TagDefinition, is_tag_in_soup, is_text_in_tag


class ExistingStringInTag(BaseModel):
    include_string: str
    tag: TagDefinition


class ValidationConfig(BaseModel):
    existing_tags: Optional[List[TagDefinition]] = None
    existing_strings_in_tags: Optional[List[ExistingStringInTag]] = None


class SoapValidator:
    def __init__(
        self, soup: BeautifulSoup, validation_config: ValidationConfig
    ):
        self.soup = soup
        self.validation_config = validation_config
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

        if self.validation_config.existing_tags:
            are_all_tags_in_soup = all(
                (
                    is_tag_in_soup(soup=self.soup, tag_definition=tag)
                    for tag in self.validation_config.existing_tags
                )
            )
        else:
            are_all_tags_in_soup = True

        if self.validation_config.existing_strings_in_tags:
            are_all_strings_in_tags = all(
                (
                    is_text_in_tag(
                        soup=self.soup,
                        tag_definition=existing_string_in_tag.tag,
                        text=existing_string_in_tag.include_string,
                    )
                    for existing_string_in_tag in self.validation_config.existing_strings_in_tags
                )
            )
        else:
            are_all_strings_in_tags = True

        self.valid = all([are_all_tags_in_soup, are_all_strings_in_tags])
