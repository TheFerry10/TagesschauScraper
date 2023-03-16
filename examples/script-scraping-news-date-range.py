"""
===============================
Scraping news data for a date range
===============================
Scraping news data for a specified date range and news category. The script
can be used as a command line tool. Arguments will be parser from the CLI.
"""

import argparse
import logging
import time
import os
import json
from datetime import datetime
from tagesschauscraper import helper, tagesschau
from tagesschauscraper.tagesschau import ARCHIVE_URL

# Argument parsing
parser = argparse.ArgumentParser(
    prog="TagesschauScraperDateRange",
    description=(
        "This script scrapes news data from Tagesschau.de. The scraped news"
        " are filtered by date range and news category."
    ),
)
parser.add_argument(
    "start_date",
    metavar="start",
    type=str,
    help=(
        "Start date for date range (inclusive). Accepted date format is"
        " YYYY-MM-DD"
    ),
)
parser.add_argument(
    "end_date",
    metavar="end",
    type=str,
    help=(
        "End date for date range (exclusive). Accepted date format is"
        " YYYY-MM-DD"
    ),
)
parser.add_argument(
    "--category",
    type=str,
    help="Filter news article by news category",
    default="all",
    choices=["wirtschaft", "inland", "ausland", "all"],
)
parser.add_argument(
    "--datadir",
    type=str,
    help="Output dir",
    default="data",
)
parser.add_argument(
    "--logdir",
    type=str,
    help="Log dir",
    default="logs",
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)
args = parser.parse_args()

# Set up logging
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)
log_file = helper.create_file_name_from_date(
    datetime.now(), suffix="scrape", extension=".log"
)
logging.basicConfig(
    filename=os.path.join(args.logdir, log_file),
    level=logging.DEBUG if args.verbose else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

start_time = time.time()
input_date_pattern = "%Y-%m-%d"
start_date = datetime.strptime(args.start_date, input_date_pattern).date()
end_date = datetime.strptime(args.end_date, input_date_pattern).date()
dates = helper.get_date_range(start_date=start_date, end_date=end_date)

logging.info(
    f"Initialize scraping for date range ({args.start_date}, {args.end_date})"
    " and category {args.category}"
)
archiveFilters = [
    tagesschau.ArchiveFilter({"date": date_, "category": args.category})
    for date_ in dates
]
config = tagesschau.ScraperConfig(archiveFilters)
tagesschauScraper = tagesschau.TagesschauScraper()
logging.info(
    f"Scraping news from URL {ARCHIVE_URL} with params {config.request_params}"
)
records = tagesschauScraper.get_news_from_archive(config)
logging.info("Scraping terminated.")

if not os.path.isdir(args.datadir):
    os.mkdir(args.datadir)

file_name = "_".join([args.start_date, args.end_date, args.category]) + ".json"
file_name_and_path = os.path.join(args.datadir, file_name)
logging.info(f"Save scraped news to file {file_name_and_path}")
with open(file_name_and_path, "w") as fp:
    json.dump(records, fp, indent=4)
logging.info("Done.")
end_time = time.time()
logging.info(f"Execution time: {end_time - start_time:.2f} seconds")
