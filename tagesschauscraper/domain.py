from tagesschauscraper.archive import Archive, ArchiveFilter, get_archive_html
from tagesschauscraper.teaser import Teaser


def scrape_teaser(archive_filter: ArchiveFilter) -> list:
    archive_html = get_archive_html(archive_filter)
    archive = Archive(archive_html)
    return [
        Teaser(raw_teaser).extract() for raw_teaser in archive.extract_teaser_list()
    ]
