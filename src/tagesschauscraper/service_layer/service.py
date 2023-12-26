import datetime
from typing import List, Optional

from tagesschauscraper.domain.archive import Archive, ArchiveFilter, get_archive_html
from tagesschauscraper.domain.article import Article, ArticleScraper, get_article_html
from tagesschauscraper.domain.teaser import Teaser, TeaserScraper


def scrape_teaser(
    archive_filter: ArchiveFilter,
    extraction_timestamp: Optional[datetime.datetime] = None,
) -> List[Teaser]:
    archive_html = get_archive_html(archive_filter)
    archive = Archive(archive_html)
    return [
        TeaserScraper(raw_teaser).extract(extraction_timestamp)
        for raw_teaser in archive.extract_teaser_list()
    ]


def scrape_article(
    teaser_list: List[Teaser],
    extraction_timestamp: Optional[datetime.datetime] = None,
) -> List[Article]:
    article_list: List[Article] = []
    for t in teaser_list:
        raw_article = get_article_html(t.article_link)
        article = ArticleScraper(raw_article).extract(extraction_timestamp)
        article.article_link = t.article_link
        article_list.append(article)
    return article_list
