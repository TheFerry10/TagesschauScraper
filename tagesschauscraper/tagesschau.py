import sqlite3
from datetime import date
from typing import Dict, Union
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from tagesschauscraper import constants, helper, retrieve

ARCHIVE_URL = "https://www.tagesschau.de/archiv/"
NEWS_CATEGORIES = ["wirtschaft", "inland", "ausland"]
RequestParams = Dict[str, str]
TeaserRecord = Dict[str, str]
ArticleRecord = Dict[str, str]
NewsId = str
NewsRecord = Dict[str, Union[NewsId, TeaserRecord, ArticleRecord]]


class ArchiveFilter:
    """
    Class for encapsulating the filter options for the news archive.

    Filtering the archive on <date_>, <category> and <page> are implemented.
    The main purpose of the ArchiveFilter is to abstract implementation details
    regarding filtering news.
    """

    PARAMS_KEY_MAPPING = {
        "date": "datum",
        "category": "ressort",
        "page": "pageIndex",
    }

    def __init__(self, raw_params: Dict[str, Union[str, date]]) -> None:
        """
        Processing the parameters internally after providing the unprocessed
        parameters as input.

        Parameters
        ----------
        raw_params : Dict[str, Union[str, date]]
            Unprocessed parameters
        """
        self.raw_params = raw_params
        self.processed_params = self.process_params(raw_params)

    def process_date(self, date_: date) -> str:
        self.DATE_PATTERN = "%Y-%m-%d"
        date_str = date_.strftime(self.DATE_PATTERN)
        return date_str

    def process_category(
        self,
        category: str,
    ) -> str:
        if category in NEWS_CATEGORIES:
            return category
        else:
            return ""

    def process_page(self, page: str = "1") -> str:
        if page.isdigit():
            return page
        else:
            return ""

    def choose_process_logic(
        self, param_name: str, param_value: Union[date, str]
    ) -> str:
        """
        Return the processed parameter value based on the parameter name. This
        function is a wrapper for the implemented processing functions.

        Parameters
        ----------
        param_name : str
            Parameter name
        param_value : Union[date, str]
            Parameter value

        Returns
        -------
        str
            Processed parameter value according to processing function.

        Raises
        ------
        ValueError
            Raise error when processing function not implemented for parameter
            value.
        """
        if (param_name == "date") and isinstance(param_value, date):
            return self.process_date(param_value)
        elif (param_name == "category") and isinstance(param_value, str):
            return self.process_category(param_value)
        elif (param_name == "page") and isinstance(param_value, str):
            return self.process_page(param_value)
        else:
            raise ValueError

    def process_params(
        self, raw_params: Dict[str, Union[str, date]]
    ) -> RequestParams:
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


class TagesschauConfig:
    """
    A configuration class for the TagesschauScraper.
    """

    def __init__(
        self, archive_filter: Union[ArchiveFilter, list[ArchiveFilter]]
    ) -> None:
        """
        Generating the request parameters from the provided ArchiveFilter. It
        takes also into account when results span multiple pages.

        Parameters
        ----------
        archive_filter : Union[ArchiveFilter, list[ArchiveFilter]]
            The ArchiveFilter object (or list of ArchiveFilters) abstracts the
            search criteria for the scraping process.
        """
        if not isinstance(archive_filter, list):
            self.archive_filters = [archive_filter]
        else:
            self.archive_filters = archive_filter

        self.request_params = []
        for f in self.archive_filters:
            self.request_params.extend(
                self.extend_request_params_with_pagination(f.processed_params)
            )

    def get_archive_soup_from_params(
        self, params: RequestParams
    ) -> BeautifulSoup:
        response = requests.get(ARCHIVE_URL, params=params)
        return retrieve.get_soup(response)

    def extend_request_params_with_pagination(
        self, request_params: RequestParams
    ) -> list[RequestParams]:
        """
        Extend the request parameters with a pageIndex, if the results are
        distributed over multiple pages.

        Parameters
        ----------
        request_params : RequestParams
            Initial request parameters

        Returns
        -------
        list[RequestParams]
            Expanding the request parameters to a list of request parameters.
            The length of the list is equal to the number of pages that the
            results are distributed over.
        """
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

    def get_news_from_archive(
        self, config: TagesschauConfig
    ) -> Dict[str, list[NewsRecord]]:
        records = []
        for params in config.request_params:
            response = requests.get(ARCHIVE_URL, params=params)
            records.extend(
                self.scrape_teaser_and_articles(response)["records"]
            )
        return {"records": records}

    def scrape_teaser(
        self, response: requests.Response
    ) -> Dict[str, list[TeaserRecord]]:
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
        if websiteTest.is_element(attrs=self.validation_element):
            return self._extract_all_teaser(websiteTest.soup)
        else:
            raise ValueError(
                f"HTML element with specifications {self.validation_element}  "
                "cannot be found."
            )

    def scrape_teaser_and_articles(
        self, response: requests.Response
    ) -> Dict[str, list[NewsRecord]]:
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
    ) -> Dict[str, list[TeaserRecord]]:
        self.teaser_element = {
            "class": "columns teaser-xs twelve teaser-xs__wide"
        }
        extracted_teaser_list: list[TeaserRecord] = []
        for teaser in soup.find_all(attrs=self.teaser_element):
            teaserObj = Teaser(soup=teaser)
            teaser_data = teaserObj.get_data()
            if teaserObj.is_extracted_data_valid(teaser_data):
                extracted_teaser_list.append(teaser_data)
        return {"records": extracted_teaser_list}

    def _merge_teaser_and_article_tags(
        self, teaser_data: TeaserRecord
    ) -> NewsRecord:
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
        if article_link:
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
        else:
            raise ValueError("No article link found in provided teaser data.")


class TagesschauContent:
    """
    Base class for dealing with different content on Tagesschau.de.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup
        self.html_mapping: Dict[str, Dict[str, Union[Dict[str, str], str]]] = (
            {}
        )
        self.extracted_data: Dict[str, Union[str, list[str]]] = {}

    def get_data(self) -> Dict[str, Union[str, list[str]]]:
        self.extract_data()
        self.process_extracted_data()
        self.check_extracted_data()
        return self.extracted_data

    def extract_data(self) -> None:
        """
        Extracts structured information from soup.

        Returns
        -------
        dict
            A dictionary containing all structured information.
        """
        for name, attrs_and_type in self.html_mapping.items():
            results = self.soup.find_all(attrs=attrs_and_type["attrs"])
            extracted_results: list[str] = []
            for tag in results:
                if isinstance(tag, Tag):
                    if attrs_and_type["type"] == "text":
                        r = tag.get_text(strip=True, separator=" ")
                        extracted_results.append(r)

                    elif attrs_and_type["type"] == "href":
                        href = tag.get("href")
                        if isinstance(href, str):
                            r = href
                            extracted_results.append(r)
                        else:
                            raise ValueError
            if len(extracted_results) == 1:
                self.extracted_data[name] = extracted_results[0]
            else:
                self.extracted_data[name] = extracted_results

        return

    def process_extracted_data(self) -> None:
        pass

    def check_extracted_data(self) -> None:
        if not self.is_extracted_data_valid():
            raise ValueError

    def is_extracted_data_valid(self) -> bool:
        return True


class Archive(TagesschauContent):
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
        self.archive_info: Dict[str, str] = dict()
        self.html_mapping = {
            "headline": {
                "attrs": {"class": "archive__headline"},
                "type": "text",
            },
            "num_teaser": {
                "attrs": {"class": "ergebnisse__anzahl"},
                "type": "text",
            },
            "current_page": {"attrs": {"class": "active"}, "type": "text"},
            "available_pages": {
                "attrs": {"class": "paginierung__liste--link"},
                "type": "text",
            },
        }
        self.extracted_data: Dict[str, Union[str, list[str]]] = {}

    def process_extracted_data(self) -> None:
        if self.extracted_data.get("available_pages"):
            r = self.extracted_data.get("available_pages")
            if isinstance(r, list):
                max_page_number = max([int(p) for p in r if p.isdigit()])
                self.extracted_data["available_pages"] = [
                    {"pageIndex": str(p)}
                    for p in range(1, max_page_number + 1)
                ]
            elif isinstance(r, str) and r.isdigit():
                self.extracted_data["available_pages"] = [{"pageIndex": r}]

        else:
            self.extracted_data["available_pages"] = [{"pageIndex": 1}]

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


class Teaser(TagesschauContent):
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
        self.soup = soup
        self.extracted_data: Dict[str, Union[str, list[str]]] = {}
        self.required_attributes = {
            "date",
            "topline",
            "headline",
            "shorttext",
            "link",
        }
        self.html_mapping = {
            "date": {"attrs": {"class": "teaser-xs__date"}, "type": "text"},
            "topline": {
                "attrs": {"class": "teaser-xs__topline"},
                "type": "text",
            },
            "headline": {
                "attrs": {"class": "teaser-xs__headline"},
                "type": "text",
            },
            "shorttext": {
                "attrs": {"class": "teaser-xs__shorttext"},
                "type": "text",
            },
            "link": {"attrs": {"class": "teaser-xs__link"}, "type": "href"},
        }

    def process_extracted_data(self) -> None:
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
        if self.extracted_data.get("date"):
            if isinstance(self.extracted_data["date"], str):
                self.extracted_data["date"] = helper.transform_datetime_str(
                    self.extracted_data["date"]
                )
        else:
            pass

    def is_extracted_data_valid(self) -> bool:
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
        if not self.required_attributes.difference(self.extracted_data.keys()):
            return True
        else:
            return False


class Article(TagesschauContent):
    """
    A class for extracting information from news article HTML elements.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.article_soup = soup
        self.html_mapping = {
            "tags": {
                "attrs": {"class": "tag-btn tag-btn--light-grey"},
                "type": "text",
            }
        }
        self.extracted_data: Dict[str, Union[str, list[str]]] = {}

    def process_extracted_data(self):
        if self.extracted_data.get("tags"):
            if isinstance(self.extracted_data["tags"], list):
                self.extracted_data["tags"] = ",".join(
                    sorted(self.extracted_data["tags"])
                )
            else:
                self.extracted_data["tags"] = [self.extracted_data["tags"]]
        else:
            pass


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

    def insert(self, content: Dict[str, str]) -> None:
        query = f"""
            INSERT OR IGNORE INTO {TagesschauDB._TABLE_NAME}
            VALUES (:id, :date, :topline, :headline, :shorttext, :link, :tags)
            """
        with self.conn:
            self.c.execute(query, content)
