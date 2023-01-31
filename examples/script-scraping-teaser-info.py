"""
===============================
Scraping teaser information
===============================
Scraping teaser information for a specified date and news category. The script can be used as a command line tool. Arguments will be parser from the CLI.
"""

import argparse
import logging
import time
import os
from datetime import datetime
from tagesschauscraper import constants, helper, tagesschau

# Arguemnt parsing
parser = argparse.ArgumentParser(
    prog="TagesschauScraper",
    description=(
        "This script scrapes news teaser from Tagesschau.de. The scraped news"
        " teaser are filtered by publishing date and news category."
    ),
)
parser.add_argument(
    "date",
    metavar="d",
    type=str,
    help=(
        "Filter teaser by publishing date. Accepted date format is YYYY-MM-DD"
    ),
)
parser.add_argument(
    "--category",
    type=str,
    help="Filter teaser by news category",
    default="all",
    choices=["wirtschaft", "inland", "ausland", "all"],
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)
args = parser.parse_args()

# Set up logging
if not os.path.exists(constants.log_dir):
    os.makedirs(constants.log_dir)
log_file = helper.create_file_name_from_date(
    datetime.now(), suffix="scrape", extension=".log"
)
logging.basicConfig(
    filename=os.path.join(constants.log_dir, log_file),
    level=logging.DEBUG if args.verbose else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


start_time = time.time()

input_date_pattern = "%Y-%m-%d"
date_ = datetime.strptime(args.date, input_date_pattern).date()
category = args.category

logging.info(
    f"Initialize scraping for date {args.date} and category {args.category}"
)
tagesschauScraper = tagesschau.TagesschauScraper()
url = tagesschau.create_url_for_news_archive(date_, category=category)
logging.info(f"Scraping teaser from URL {url}")
teaser = tagesschauScraper.scrape_teaser(url)
logging.info("Scraping terminated.")

dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(date_)
file_path = os.path.join(
    dateDirectoryTreeCreator.path,
    helper.create_file_name_from_date(
        date_, suffix="_" + category, extension=".json"
    ),
)
logging.info(f"Save scraped teaser to file {file_path}")
helper.save_to_json(teaser, file_path)
logging.info("Done.")
end_time = time.time()
logging.info(f"Execution time: {end_time - start_time:.2f} seconds")
