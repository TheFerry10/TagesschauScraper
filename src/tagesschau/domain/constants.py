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
ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")
ARTICLE_TEST_DATA_DIR = Path("tests/data/article/")
TEASER_TEST_DATA_DIR = Path("tests/data/teaser/")
TEST_DATA_DIR = Path("tests/data/")
TEST_CONFIG_DIR = Path("tests/data/config/")
TEASER_CONFIG_PATH = Path("src/tagesschauscraper/teaser-config.yml")
