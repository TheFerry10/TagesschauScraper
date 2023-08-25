import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.models import Response
from typing import Dict, Union


def get_soup_from_url(url: str) -> BeautifulSoup:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError
    return BeautifulSoup(response.text, "html.parser")


def get_soup(response: Response) -> BeautifulSoup:
    if response.status_code != 200:
        raise ValueError
    return BeautifulSoup(response.text, "html.parser")


def get_text_from_html(
    soup: BeautifulSoup, element: Dict[str, str], separator: str = "\n"
) -> Union[str, None]:
    html_element = soup.find(attrs=element)
    if isinstance(html_element, Tag):
        return html_element.get_text(strip=True, separator=separator)
    else:
        return None


def get_link_from_html(
    soup: BeautifulSoup, element: Dict[str, str]
) -> Union[str, None]:
    html_element = soup.find(attrs=element)
    if isinstance(html_element, Tag):
        result = html_element.get("href")
        if isinstance(result, str):
            return result
    return None


class WebsiteTest:
    """
    Testing if a website works as expected.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def is_element(
        self,
        name: Union[str, None] = None,
        attrs: Dict[str, str] = {},
        **kwargs: Dict[str, str],
    ) -> bool:
        """
        Check if html element exists on website.
        """
        if self.soup.find(
            name=name, attrs=attrs, recursive=True, string=None, **kwargs
        ):
            return True
        else:
            return False

    def is_text_in_element(
        self,
        target_text: str,
        name: Union[str, None] = None,
        attrs: Dict[str, str] = {},
        **kwargs: Dict[str, str],
    ) -> bool:
        """
        Check if text is in html element.
        """
        result = self.soup.find(
            name=name, attrs=attrs, recursive=True, string=None, **kwargs
        )
        if result:
            return target_text in result.get_text()
        else:
            return False
