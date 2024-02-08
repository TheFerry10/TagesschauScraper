from pathlib import Path

GERMAN_MONTHS = [
    "",
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
]
ARCHIVE_URL = "https://www.tagesschau.de/archiv"
TAGESSCHAU_URL = "https://www.tagesschau.de"
NEWS_CATEGORIES = ["wirtschaft", "inland", "ausland"]
TEST_HTML_DIR = Path("tests/data/tagesschau/html/")
TEST_CONFIG_DIR = Path("tests/data/tagesschau/config/")
ARCHIVE_HTML_PATH = TEST_HTML_DIR.joinpath("archive.html")
TEASER_HTML_PATH = TEST_HTML_DIR.joinpath("teaser.html")
ARTICLE_HTML_PATH = TEST_HTML_DIR.joinpath("article.html")
ARTICLE_CONFIG_YAML = TEST_CONFIG_DIR.joinpath("article-config.yml")
TEASER_CONFIG_YAML = TEST_CONFIG_DIR.joinpath("teaser-config.yml")
ARCHIVE_CONFIG_YAML = TEST_CONFIG_DIR.joinpath("archive-config.yml")
DEFAULT_DATE_PATTERN = "%Y-%m-%d"
