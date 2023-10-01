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


def cast_to_list(input_: object) -> list[object]:
    if not isinstance(input_, list):
        return [input_]
    return input_


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


def create_request_params(archive_filter: ArchiveFilter) -> dict:
    return {
        "datum": transform_date(archive_filter.date),
        "filter": archive_filter.news_category,
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


@dataclass
class TagDefinition:
    name: str
    attrs: Dict[str, str]


def is_tag_in_soup(soup: BeautifulSoup, tag_definition: TagDefinition) -> bool:
    if soup.find(name=tag_definition.name, attrs=tag_definition.attrs):
        return True
    return False


def is_text_in_tag(
    soup: BeautifulSoup,
    tag_definition: TagDefinition,
    text: str,
) -> bool:
    tag = soup.find(tag_definition.name, tag_definition.attrs)
    if tag:
        return text in tag.get_text(strip=True)
    return False


class NotValidHTML(Exception):
    pass


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

    # TODO: Better define this in a separate config file
    RequiredHTMLContent = {
        "tagDefinition": TagDefinition("div", {"class": "trenner__text__topline"}),
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

    def extract_teaser_list(self) -> None:
        pass

    def extract_news_categories(self) -> set:
        # TODO Check existence of category container
        category_container = self.soup.find("ul", {"class": "tabnav__list swipe"})
        categories: set[str] = set()
        if isinstance(category_container, Tag):
            categories = {
                category_element.get_text(strip=True)
                for category_element in category_container.find_all(
                    "li", {"class": "tabnav__item"}
                )
            }
        return categories

    def extract_date(self) -> str:
        date_tag = self.soup.find(attrs={"class": "archive__headline"})
        if date_tag:
            return date_tag.get_text(strip=True)


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
            raise NotValidHTML(f"Not valid HTML content for {Teaser.__name__}")

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
