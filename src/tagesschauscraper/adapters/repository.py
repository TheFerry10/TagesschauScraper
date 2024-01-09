import abc
import csv
from pathlib import Path
from typing import Dict

from tagesschauscraper.domain.article import Article
from tagesschauscraper.domain.teaser import Teaser


class AbstractTeaserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, teaser: Teaser):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, article_link: str) -> Teaser:
        raise NotImplementedError


class AbstractArticleRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, article: Article):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, article_link) -> Article:
        raise NotImplementedError


class SqlAlchemyTeaserRepository(AbstractTeaserRepository):
    def __init__(self, session):
        self.session = session

    def add(self, teaser):
        self.session.add(teaser)

    def get(self, article_link):
        return (
            self.session.query(Teaser)
            .filter_by(article_link=article_link)
            .one()
        )

    def list(self):
        return self.session.query(Teaser).all()


class SqlAlchemyArticleRepository(AbstractArticleRepository):
    def __init__(self, session):
        self.session = session

    def add(self, article):
        self.session.add(article)

    def get(self, article_link):
        return (
            self.session.query(Article)
            .filter_by(article_link=article_link)
            .one()
        )

    def list(self):
        return self.session.query(Article).all()


class CsvTeaserRepository(AbstractTeaserRepository):
    def __init__(self, folder):
        self._teaser_path = Path(folder) / "teaser.csv"
        self._teasers: Dict[str, Teaser] = {}
        self._load()

    def _load(self):
        """
        Load all teaser from csv file as a dictionary
        """
        with self._teaser_path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row["date"]
                topline = row["topline"]
                headline = row["headline"]
                shorttext = row["shorttext"]
                article_link = row["article_link"]
                extraction_timestamp = row["extraction_timestamp"]
                self._teasers[article_link] = Teaser(
                    date,
                    topline,
                    headline,
                    shorttext,
                    article_link,
                    extraction_timestamp,
                )

    def add(self, teaser):
        self._teasers[teaser.article_link] = teaser

    def get(self, article_link):
        return self._teasers.get(article_link)

    def list(self):
        return list(self._teasers.values())
