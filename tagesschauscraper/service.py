from tagesschauscraper.archive import Archive, ArchiveFilter, get_archive_html
from tagesschauscraper.teaser import TeaserScraper


def scrape_teaser(archive_filter: ArchiveFilter) -> list:
    archive_html = get_archive_html(archive_filter)
    archive = Archive(archive_html)
    return [
        TeaserScraper(raw_teaser).extract()
        for raw_teaser in archive.extract_teaser_list()
    ]
