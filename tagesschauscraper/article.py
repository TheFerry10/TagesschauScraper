from __future__ import annotations

from bs4 import BeautifulSoup

from tagesschauscraper.helper import AbstractContent, TagDefinition, is_tag_in_soup


class Article(AbstractContent):
    """
    A class for extracting information from news article HTML elements.
    """

    RequiredHTMLContent = {
        "tagDefinition": TagDefinition("div", {"class": "seitenkopf__title"}),
    }

    def __init__(self, soup: BeautifulSoup) -> None:
        """
        Initializes the Teaser with the provided BeautifulSoup element.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object representing an element for a news teaser.
        """
        self.soup = soup
        self.valid = False
        self.validate()

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
        self.valid = is_tag_in_soup(
            self.soup, self.RequiredHTMLContent["tagDefinition"]
        )

    def extract(self):
        raise NotImplementedError

    def extract_topline(self):
        tag = self.soup.find(attrs={"class": "seitenkopf__topline"})
        try:
            text = tag.get_text(strip=True)
        except AttributeError:
            text = None
        return text

    def extract_headline(self):
        tag = self.soup.find(attrs={"class": "seitenkopf__headline--text"})
        try:
            text = tag.get_text(strip=True)
        except AttributeError:
            text = None
        return text

    def extract_metatextline(self):
        tag = self.soup.find(attrs={"class": "metatextline"})
        try:
            text = tag.get_text(strip=True)
        except AttributeError:
            text = None
        return text

    def extract_tags(self):
        tag = self.soup.find(attrs={"class": "taglist"})
        article_tags = tag.find_all("li", {"class": "taglist__element"})
        return [article_tag.get_text(strip=True) for article_tag in article_tags]

    def extract_subheads(self):
        tags = self.soup.find_all(
            attrs={
                "class": "meldung__subhead columns twelve m-ten m-offset-one l-eight l-offset-two liveblog--anchor"
            }
        )
        return [tag.get_text(strip=True) for tag in tags]

    def extract_paragraphs_type_one(self):
        tag = self.soup.find(
            attrs={
                "class": "textabsatz columns twelve m-ten m-offset-one l-eight l-offset-two"
            }
        )
        try:
            text = tag.get_text(strip=True)
        except AttributeError:
            text = None
        return text

    def extract_paragraphs_type_two(self):
        tag = self.soup.find(
            attrs={
                "class": "textabsatz m-ten m-offset-one l-eight l-offset-two columns twelve"
            }
        )
        try:
            text = tag.get_text(strip=True)
        except AttributeError:
            text = None
        return text
