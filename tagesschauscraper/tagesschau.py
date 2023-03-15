import sqlite3
from datetime import date
from typing import Literal, Dict, Union
import requests
from bs4 import BeautifulSoup, Tag
from tagesschauscraper import constants, helper, retrieve
from dataclasses import dataclass

ARCHIVE_URL = "https://www.tagesschau.de/archiv/"
NEWS_CATEGORIES = ["wirtschaft", "inland", "ausland"]
RequestParams = Dict[str, str]
NewsRecord = Dict[str, str]


class ArchiveFilter:
    """
    Class for encapsulating the filter options for the news archive

    Parameters
    ----------
    date_ : date
        Filter articles on date.
    category : str, optional
        Filter articles on category. Could be "wirtschaft", "inland",
        "ausland" or "all".
        By default, "all" is selected.
    page: int
        Page number. Default is 1.

    Returns
    -------
    dict
        Request parameters

    Raises
    ------
    ValueError
        When category is not defined.
    """

    PARAMS_KEY_MAPPING = {
        "date": "datum",
        "category": "ressort",
        "page": "pageIndex",
    }

    def __init__(self, raw_params: dict):
        self.raw_params = raw_params
        self.processed_params = self.process_params(raw_params)

    def process_date(self, date_: date):
        self.DATE_PATTERN = "%Y-%m-%d"
        date_str = date_.strftime(self.DATE_PATTERN)
        return date_str

    def process_category(
        self,
        category: str,
    ):
        if category in NEWS_CATEGORIES:
            return category
        else:
            return ""

    def process_page(self, page: str = "1"):
        if page.isdigit():
            return page
        else:
            return ""

    def choose_process_logic(
        self, param_name: str, param_value: Union[date, str]
    ) -> str:
        if (param_name == "date") and isinstance(param_value, date):
            return self.process_date(param_value)
        elif (param_name == "category") and isinstance(param_value, str):
            return self.process_category(param_value)
        elif (param_name == "page") and isinstance(param_value, str):
            return self.process_page(param_value)
        else:
            raise ValueError

    def process_params(self, raw_params: dict) -> RequestParams:
        """
        Process the filter parameters to strings.

        Returns
        -------
        dict
            Request parameters

        Raises
        ------
        ValueError
            When category is not defined.
        """
        return {
            ArchiveFilter.PARAMS_KEY_MAPPING[k]: self.choose_process_logic(
                k, v
            )
            for k, v in raw_params.items()
        }


class ScraperConfig:
    """
    A configuration class for the TagesschauScraper.
    """

    def __init__(
        self, archive_filter: Union[ArchiveFilter, list[ArchiveFilter]]
    ) -> None:
        if not isinstance(archive_filter, list):
            self.archive_filters = [archive_filter]
        else:
            self.archive_filters = archive_filter

        self.request_params = []
        for f in self.archive_filters:
            self.request_params.extend(
                self.extend_request_params_with_pagination(f.processed_params)
            )

    def get_archive_soup_from_params(self, params):
        response = requests.get(ARCHIVE_URL, params=params)
        return retrieve.get_soup(response)

    def extend_request_params_with_pagination(
        self, request_params: RequestParams
    ) -> list[RequestParams]:
        soup = self.get_archive_soup_from_params(request_params)
        archive = Archive(soup)
        pagination = archive.extract_pagination()
        return [request_params | p for p in pagination]


class TagesschauScraper:
    """
    A web scraper specified for scraping the news archive of Tagesschau.de.
    """

    def __init__(self) -> None:
        self.validation_element = {"class": "archive__headline"}

    def get_news_from_archive(self, config: ScraperConfig) -> dict:
        records = []
        for params in config.request_params:
            response = requests.get(ARCHIVE_URL, params=params)
            records.extend(
                self.scrape_teaser_and_articles(response)["records"]
            )
        return {"records": records}

    def scrape_teaser(self, response: requests.Response) -> dict:
        """
        Scrape all teaser on the archive <url>.

        Parameters
        ----------
        url : str
            Archive website.


        Returns
        -------
        dict
            Scraped teaser.
        """
        websiteTest = retrieve.WebsiteTest(response)
        if websiteTest.is_element(self.validation_element):
            return self._extract_all_teaser(websiteTest.soup)
        else:
            raise ValueError(
                f"HTML element with specifications {self.validation_element}  "
                "cannot be found."
            )

    def scrape_teaser_and_articles(self, response: requests.Response) -> dict:
        """
        Scrape all teaser on the archive <url>.

        Parameters
        ----------
        url : str
            Archive website.

        Returns
        -------
        dict
            Scraped teaser and article data.
        """
        all_teaser = self.scrape_teaser(response)["records"]
        teaser_and_article_data = [
            self._merge_teaser_and_article_tags(teaser_data)
            for teaser_data in all_teaser
        ]
        return {"records": teaser_and_article_data}

    def _extract_all_teaser(
        self, soup: BeautifulSoup
    ) -> Dict[str, list[NewsRecord]]:
        self.teaser_element = {
            "class": "columns teaser-xs twelve teaser-xs__wide"
        }
        extracted_teaser_list: list[NewsRecord] = []
        for teaser in soup.find_all(**self.teaser_element):
            teaserObj = Teaser(soup=teaser)
            teaser_data = teaserObj.get_data()
            if teaserObj.is_teaser_data_valid(teaser_data):
                extracted_teaser_list.append(teaser_data)
        return {"records": extracted_teaser_list}

    def _merge_teaser_and_article_tags(self, teaser_data: dict) -> dict:
        """
        Enrich the teaser information with the article tags.

        Parameters
        ----------
        teaser_info : dict
            All information extracted from the news teaser.

        Returns
        -------
        dict
            Dictionary containing news teaser information enriched by article
            tags.
        """
        article_link = teaser_data.get("link")
        id_ = helper.get_hash_from_string(article_link)
        article_tags = {}
        if article_link:
            try:
                article_soup = retrieve.get_soup_from_url(article_link)

            except requests.exceptions.TooManyRedirects:
                print(f"Article not found for link: {article_link}.")

            else:
                articleObj = Article(article_soup)
                article_tags = articleObj.extract_article_tags()
        article_data = article_tags
        return {"id": id_, "teaser": teaser_data, "article": article_data}


class Archive:
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
        self.archive_soup = soup
        self.archive_info: Dict[str, str] = dict()

    def get_all_teaser(self):
        ...

    def extract_pagination(self) -> list[Dict[str, str]]:
        page_keyword = "pageIndex"
        pagination_html = self.archive_soup.find(
            "ul", class_="paginierung__liste"
        )
        max_page = 1
        if isinstance(pagination_html, Tag):
            pagination_elements = pagination_html.find_all("li")
            if pagination_elements:
                for element in pagination_elements:
                    if hasattr(element, "get_text"):
                        try:
                            page = int(element.get_text(strip=True))
                        except ValueError:
                            print(
                                "Cannot cast str to int for"
                                f" '{element.get_text(strip=True)}'. Continue"
                                " execution."
                            )
                        else:
                            if page > max_page:
                                max_page = page
        return [{page_keyword: str(p)} for p in range(1, max_page + 1)]

    def transform_date_to_date_in_headline(self, date_: date) -> str:
        year = date_.year
        month = date_.month
        day = date_.day
        return f"{day}. {constants.german_month_names[month]} {year}"

    def transform_date_in_headline_to_date(
        self, date_in_headline: str
    ) -> date:
        day_raw, month_raw, year_raw = date_in_headline.split()
        day = int(day_raw[:-1])
        month = constants.german_month_names.index(month_raw)
        year = int(year_raw)
        return date(year, month, day)

    def extract_info_from_archive(self) -> dict:
        name_html_mapping_text = {
            "headline": "archive__headline",
            "num_teaser": "ergebnisse__anzahl",
        }
        self.archive_info = {
            name: retrieve.get_text_from_html(
                self.archive_soup, {"class_": html_tag}
            )
            for name, html_tag in name_html_mapping_text.items()
        }
        return self.archive_info


class Teaser:
    """
    A class for extracting information from news teaser elements.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.teaser_soup = soup
        self.teaser_info: Dict[str, str] = dict()
        self.required_attributes = {
            "date",
            "topline",
            "headline",
            "shorttext",
            "link",
        }

    def get_data(self) -> NewsRecord:
        extracted_data = self.extract_data_from_teaser()
        return self.process_extracted_data(extracted_data)

    def extract_data_from_teaser(self) -> dict:
        """
        Extracts structured information from a teaser element.
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
        field_names_text = ["date", "topline", "headline", "shorttext"]
        field_names_link = ["link"]
        name_html_mapping = {
            key: f"teaser-xs__{key}"
            for key in field_names_text + field_names_link
        }

        for field_name, html_class_name in name_html_mapping.items():
            tag = self.teaser_soup.find(class_=html_class_name)
            if isinstance(tag, Tag):
                if field_name in field_names_text:
                    self.teaser_info[field_name] = tag.get_text(
                        strip=True, separator=" "
                    )
                elif field_name in field_names_link:
                    if isinstance(tag.get("href"), str):
                        self.teaser_info[field_name] = tag.get("href")  # type: ignore
                    else:
                        raise ValueError

        return self.teaser_info

    def process_extracted_data(self, teaser_info: dict) -> dict:
        """
        Process the extracted teaser information.

        Parameters
        ----------
        teaser_info : dict
            Dictionary containing news teaser information.

        Returns
        -------
        dict
            Dictionary containing processed teaser information.
        """
        teaser_info["date"] = helper.transform_datetime_str(
            teaser_info["date"]
        )
        self.teaser_info.update(teaser_info)
        return teaser_info

    def is_teaser_data_valid(self, teaser_info: Dict[str, str]) -> bool:
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
        if not self.required_attributes.difference(teaser_info.keys()):
            return True
        else:
            return False


class Article:
    """
    A class for extracting information from news article HTML elements.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.article_soup = soup
        self.tags_element = {"class": "taglist"}

    def get_data(self) -> Dict[str, str]:
        article_tags = self.extract_article_tags()
        article_data = article_tags
        return article_data

    def extract_article_tags(self) -> Dict[str, str]:
        tags_group = self.article_soup.find(class_="taglist")
        if isinstance(tags_group, Tag):
            tags = [
                tag.get_text(strip=True)
                for tag in tags_group.find_all(
                    class_="tag-btn tag-btn--light-grey"
                )
                if hasattr(tag, "get_text")
            ]
        else:
            tags = []
        return {"tags": ",".join(sorted(tags))}


class TagesschauDB:
    _DB_NAME = "news.db"
    _TABLE_NAME = "Tagesschau"

    def __init__(self) -> None:
        self.connect()

    def connect(self) -> None:
        self.conn = sqlite3.connect(TagesschauDB._DB_NAME)
        self.c = self.conn.cursor()
        print(f"Connected to {TagesschauDB._DB_NAME}")

    def create_table(self) -> None:
        query = f"""
            CREATE TABLE IF NOT EXISTS  {TagesschauDB._TABLE_NAME} (
            id text UNIQUE,
            timestamp datetime,
            topline text,
            headline text,
            shorttext text,
            link text,
            tags text)
            """
        self.c.execute(query)

    def drop_table(self) -> None:
        query = f"""
            DROP TABLE IF EXISTS {TagesschauDB._TABLE_NAME}
            """
        self.c.execute(query)

    def insert(self, content: dict) -> None:
        query = f"""
            INSERT OR IGNORE INTO {TagesschauDB._TABLE_NAME}
            VALUES (:id, :date, :topline, :headline, :shorttext, :link, :tags)
            """
        with self.conn:
            self.c.execute(query, content)
