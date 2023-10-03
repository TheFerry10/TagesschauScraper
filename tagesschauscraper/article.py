from __future__ import annotations
from bs4 import BeautifulSoup
from tagesschauscraper.helper import AbstractContent


class Article(AbstractContent):
    """
    A class for extracting information from news article HTML elements.
    """

    def __init__(self, soup: BeautifulSoup) -> None:
        self.article_soup = soup
        self.tags_element = {"class": "taglist"}

    # def is_valid(self) -> bool:
    #     test = WebsiteTest(self.article_soup)
    #     required_elements = [
    #         {"class": "seitenkopf__title"},
    #         {"class": "seitenkopf__headline"},
    #         {"class": "taglist"},
    #     ]
    #     return any([test.is_element(attrs=r) for r in required_elements])

    # def get_data(self):
    #     article_tags = self.extract_article_tags()
    #     article_data = article_tags
    #     return article_data

    # def extract_article_tags(self):
    #     tags_group = self.article_soup.find(class_="taglist")
    #     if isinstance(tags_group, Tag):
    #         tags = [
    #             tag.get_text(strip=True)
    #             for tag in tags_group.find_all(class_="tag-btn tag-btn--light-grey")
    #             if hasattr(tag, "get_text")
    #         ]
    #     else:
    #         tags = []
    #     return {"tags": ",".join(sorted(tags))}
