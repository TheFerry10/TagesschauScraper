from __future__ import annotations
from datetime import date
from typing import Dict, Union, List
from bs4 import BeautifulSoup
from bs4.element import Tag
from tagesschauscraper import constants, helper
from tagesschauscraper.retrieve import WebsiteTest
from dataclasses import dataclass
import abc


ARCHIVE_URL = "https://www.tagesschau.de/archiv/"
NEWS_CATEGORIES = ["wirtschaft", "inland", "ausland"]
DEFAULT_DATE_PATTERN = "%Y-%m-%d"


#TODO move to utils
def cast_to_list(input: object) -> list[object]:
    if not isinstance(input, list):
        return [input]
    else:
        return input

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

@dataclass(frozen=True)
class ArchiveFilter:
    date: date
    news_category: str


def is_selected_in_categories(
    category: str,
) -> bool:
    return category in NEWS_CATEGORIES


def create_request_params(archiveFilter: ArchiveFilter) -> dict:
    return {
        "datum": transform_date(archiveFilter.date),
        "filter": archiveFilter.news_category,
    }




def extract_pagination(soup: BeautifulSoup) -> list[Dict[str, str]]:
    page_keyword = "pageIndex"
    pagination_html = soup.find("ul", class_="paginierung__liste")
    max_page = 1
    if isinstance(pagination_html, Tag):
        pagination_elements = pagination_html.find_all("li")
        if pagination_elements:
            for element in pagination_elements:
                if isinstance(element, Tag):
                    page_str = element.get_text(strip=True)
                    if page_str.isdigit():
                        page = int(page_str)
                        if page > max_page:
                            max_page = page
    return [{page_keyword: str(p)} for p in range(1, max_page + 1)]


class AbstractContent(abc.ABC):
    
    @abc.abstractmethod
    def validate(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def extract(self):
        raise NotImplementedError    
        

class Archive(AbstractContent):
    """
    A class for extracting information from news archive.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup

    def validate(self) -> None:
        pass

    def extract(self) -> None:
        pass


def required_attributes_exist(soup):
    return is_text_in_element(soup, "Archiv", "div", {"class": "trenner__text__topline"})
    



def is_element(
    soup: BeautifulSoup,
    name: Union[str, None] = None,
    attrs: Dict[str, str] = {},
    **kwargs: Dict[str, str],
) -> bool:
    """
    Check if html element exists on website.
    """
    if soup.find(
        name=name, attrs=attrs, recursive=True, string=None, **kwargs
    ):
        return True
    else:
        return False

def is_text_in_element(
    soup: BeautifulSoup,
    target_text: str,
    name: Union[str, None] = None,
    attrs: Dict[str, str] = {},
) -> bool:
    """
    Check if text is in html element.
    """
    result = soup.find(
        name=name, attrs=attrs
    )
    if result:
        return target_text in result.get_text()
    else:
        return False



class NotValidHTML(Exception):
    pass

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
        if required_attributes_exist(self.soup):
            self.is_valid = True
        else:
            self.is_valid = False
            raise NotValidHTML(f'Not valid HTML content for {Teaser.__name__}')
        
    
        
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



class Article:
    """
    A class for extracting information from news article HTML elements.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.article_soup = soup
        self.tags_element = {"class": "taglist"}
        self.valid = self.is_valid()
        if not self.valid:
            raise ValueError("Article is not valid")

    def is_valid(self) -> bool:
        test = WebsiteTest(self.article_soup)
        required_elements = [
            {"class": "seitenkopf__title"},
            {"class": "seitenkopf__headline"},
            {"class": "taglist"},
        ]
        return any([test.is_element(attrs=r) for r in required_elements])

    def get_data(self):
        article_tags = self.extract_article_tags()
        article_data = article_tags
        return article_data

    def extract_article_tags(self):
        tags_group = self.article_soup.find(class_="taglist")
        if isinstance(tags_group, Tag):
            tags = [
                tag.get_text(strip=True)
                for tag in tags_group.find_all(class_="tag-btn tag-btn--light-grey")
                if hasattr(tag, "get_text")
            ]
        else:
            tags = []
        return {"tags": ",".join(sorted(tags))}
