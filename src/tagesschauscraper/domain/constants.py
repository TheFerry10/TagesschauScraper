from pathlib import Path

import yaml

german_month_names = [
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
DEFAULT_DATE_PATTERN = "%Y-%m-%d"
DEFAULT_TIMEOUT = 5
ARCHIVE_TEST_DATA_DIR = Path("tests/data/archive/")
ARTICLE_TEST_DATA_DIR = Path("tests/data/article/")
TEASER_TEST_DATA_DIR = Path("tests/data/teaser/")
TEASER_CONFIG_PATH = Path("src/tagesschauscraper/teaser-config.yml")
