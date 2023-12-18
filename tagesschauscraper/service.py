import datetime
from typing import List, Union

from tagesschauscraper.archive import Archive, ArchiveFilter, get_archive_html
from tagesschauscraper.teaser import Teaser, TeaserScraper


def scrape_teaser(
    archive_filter: ArchiveFilter,
    extraction_timestamp: Union[datetime.datetime, None] = None,
) -> List[Teaser]:
    archive_html = get_archive_html(archive_filter)
    archive = Archive(archive_html)
    return [
        TeaserScraper(raw_teaser).extract(extraction_timestamp)
        for raw_teaser in archive.extract_teaser_list()
    ]
