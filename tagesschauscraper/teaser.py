from __future__ import annotations
from typing import Union
from bs4 import BeautifulSoup
from tagesschauscraper.helper import AbstractContent


class Teaser(AbstractContent):
    """
    A class for extracting information from news teaser elements.
    """

    REQUIRED_ATTRIBUTES = []

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup
        self.is_valid: Union[None, bool] = None

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

    def extract(self):
        pass

    # def get_data(self):
    #     extracted_data = self.extract_data_from_teaser()
    #     return self.process_extracted_data(extracted_data)

    # def extract_data_from_teaser(self):
    #     """
    #     Extracts structured information from a teaser element.
    #     The extracted elements are:
    #     * date
    #     * topline
    #     * headline
    #     * shorttext
    #     * article link

    #     Returns
    #     -------
    #     dict
    #         A dictionary containing all the information of the news teaser
    #     """
    #     field_names_text = ["date", "topline", "headline", "shorttext"]
    #     field_names_link = ["link"]
    #     name_html_mapping = {
    #         key: f"teaser-xs__{key}" for key in field_names_text + field_names_link
    #     }

    #     for field_name, html_class_name in name_html_mapping.items():
    #         tag = self.teaser_soup.find(class_=html_class_name)
    #         if isinstance(tag, Tag):
    #             if field_name in field_names_text:
    #                 self.teaser_info[field_name] = tag.get_text(
    #                     strip=True, separator=" "
    #                 )
    #             elif field_name in field_names_link:
    #                 if isinstance(tag.get("href"), str):
    #                     self.teaser_info[field_name] = tag.get("href")  # type: ignore
    #                 else:
    #                     raise ValueError

    #     return self.teaser_info

    # def process_extracted_data(self, teaser_data):
    #     """
    #     Process the extracted teaser information.

    #     Parameters
    #     ----------
    #     teaser_info : dict
    #         Dictionary containing news teaser information.

    #     Returns
    #     -------
    #     dict
    #         Dictionary containing processed teaser information.
    #     """
    #     teaser_data["date"] = helper.transform_datetime_str(teaser_data["date"])
    #     self.teaser_info.update(teaser_data)
    #     return teaser_data
