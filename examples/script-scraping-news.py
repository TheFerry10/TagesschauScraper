"""
===============================
Scraping news data
===============================
Scraping news data for a specified date and news category. The script
can be used as a command line tool. Arguments will be parser from the CLI.
"""

import argparse
import logging
import time
import os
from datetime import datetime
from tagesschauscraper import helper, tagesschau
from tagesschauscraper.tagesschau import ARCHIVE_URL

# Argument parsing
parser = argparse.ArgumentParser(
    prog="TagesschauScraper",
    description=(
        "This script scrapes news data from Tagesschau.de. The scraped news"
        " are filtered by publishing date and news category."
    ),
)
parser.add_argument(
    "date",
    metavar="d",
    type=str,
    help=(
        "Filter news article by publishing date. Accepted date format is YYYY-MM-DD"
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
date_ = datetime.strptime(args.date, input_date_pattern).date()

logging.info(
    f"Initialize scraping for date {args.date} and category {args.category}"
)
archiveFilter = tagesschau.ArchiveFilter(
    {"date": date_, "category": args.category}
)
config = tagesschau.ScraperConfig(archiveFilter)
tagesschauScraper = tagesschau.TagesschauScraper()
logging.info(
    f"Scraping news from URL {ARCHIVE_URL} with params"
    f" {config.request_params}"
)
records = tagesschauScraper.get_news_from_archive(config)
logging.info("Scraping terminated.")

if not os.path.isdir(args.datadir):
    os.mkdir(args.datadir)
dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(
    date_, root_dir=args.datadir
)
file_path = dateDirectoryTreeCreator.create_file_path_from_date()
dateDirectoryTreeCreator.make_dir_tree_from_file_path(file_path)
file_name_and_path = os.path.join(
    file_path,
    helper.create_file_name_from_date(
        date_, suffix="_" + args.category, extension=".json"
    ),
)
logging.info(f"Save scraped news to file {file_name_and_path}")
helper.save_to_json(records, file_name_and_path)
logging.info("Done.")
end_time = time.time()
logging.info(f"Execution time: {end_time - start_time:.2f} seconds")
