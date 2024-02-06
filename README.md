# TagesschauScraper


Introducing "PySoupConfigScraper" – your efficient and versatile web scraping tool built with Python and BeautifulSoup. This powerful application simplifies the process of extracting structured information from HTML content, allowing you to effortlessly gather data from websites with ease.

With PySoupConfigScraper, all you need to do is provide the HTML content of the webpage you want to scrape and a configuration file that specifies the content you're interested in extracting. The configuration file acts as your guide, detailing which specific elements or tags contain the desired information.

Whether you're scraping product details, news articles, or any other structured data, PySoupConfigScraper streamlines the process, saving you valuable time and effort. Plus, its flexibility allows you to adapt to different websites and layouts by simply adjusting the configuration file.

Key Features:

Seamless HTML Parsing: Utilizes BeautifulSoup for efficient parsing of HTML content.
Configurable Extraction: Extracts targeted information based on your customized configuration file.
Structured Data Output: Outputs scraped data in a structured format, such as JSON or CSV, for easy analysis and integration into your projects.
Versatile Application: Suitable for a wide range of scraping tasks, from e-commerce product scraping to news aggregation and beyond.
Python-Powered: Leverages the simplicity and power of Python for scripting and automation.
Whether you're a data enthusiast, researcher, or developer, PySoupConfigScraper empowers you to harness the wealth of information available on the web, transforming unstructured HTML into actionable insights with precision and efficiency. Experience the convenience of targeted web scraping with PySoupConfigScraper today!

## Install
Tagesschauscraper is available on PyPI:
```sh
$ pip install tagesschauscraper
```

## Usage

Here's an example of how to use the library to scrape teaser info from the Tagesschau archive:

```python
import os
from datetime import date
from tagesschauscraper import constants, helper, tagesschau

# Scraping teaser published on <date_> and in specific news category  
DATA_DIR = "data"
date_ = date(2022,3,1)
category = "wirtschaft"

# Initialize scraper, create url and run
tagesschauScraper = tagesschau.TagesschauScraper()
url = tagesschau.create_url_for_news_archive(date_, category=category)
teaser = tagesschauScraper.scrape_teaser(url)

# Save output in a hierarchical directory tree
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(
    date_, root_dir=DATA_DIR
)
file_path = dateDirectoryTreeCreator.create_file_path_from_date()
dateDirectoryTreeCreator.make_dir_tree_from_file_path(file_path)
file_name_and_path = os.path.join(
    file_path,
    helper.create_file_name_from_date(
        date_, suffix="_" + category, extension=".json"
    ),
)
logging.info(f"Save scraped teaser to file {file_name_and_path}")
helper.save_to_json(teaser, file_name_and_path)

```
The result saved in "data/2022/03/2022-03-01_wirtschaft.json". Json document looks the following (only a snippet):
```
{
    "teaser": [
        {
            "date": "2022-03-01 22:23:00",
            "topline": "Deutliche Verluste",
            "headline": "Der Krieg lastet auf der Wall Street",
            "shorttext": "Die intensiven K\u00e4mpfe in der Ukraine und die Auswirkungen der Sanktionen verschreckten die US-Investoren.",
            "link": "https://www.tagesschau.de/wirtschaft/finanzen/marktberichte/marktbericht-dax-dow-jones-213.html",
            "tags": "B\u00f6rse,DAX,Dow Jones,Marktbericht",
            "id": "d49cfb71130e46638dcfe2afe8d775ac9670a9a8"
        },
        {
            "date": "2022-03-01 18:54:00",
            "topline": "Pipeline-Projekt",
            "headline": "Nordstream-Betreiber offenbar insolvent",
            "shorttext": "Die Nord Stream 2 AG, die Schweizer Eigent\u00fcmergesellschaft der neuen Ostsee-Pipeline nach Russland, ist offenbar insolvent.",
            "link": "https://www.tagesschau.de/wirtschaft/unternehmen/nord-stream-insolvenz-gazrom-gas-pipeline-russland-ukraine-103.html",
            "tags": "Insolvenz,Nord Stream 2,Pipeline,Russland,Schweiz",
            "id": "595aa643ed39edd3695b8401a99ce808afa539fb"
        },
        {
            "date": "2022-03-01 18:52:00",
            "topline": "Fehlende Teile wegen Ukraine-Kriegs",
            "headline": "Autobauern drohen Produktionsausf\u00e4lle",
            "shorttext": "Der anhaltende Krieg in der Ukraine bremst auch die deutsche Autoindustrie.",
            "link": "https://www.tagesschau.de/wirtschaft/autobauern-drohen-produktionsausfaelle-101.html",
            "tags": "Autowerke,BMW,Mercedes,Produktionsausf\u00e4lle,Ukraine,Ukraine-Krieg,VW",
            "id": "914174596c3590784c903908f569c099475981f7"
        },
        ...
```
## Contributing
If you'd like to contribute to TagesschauScraper, please fork the repository and make changes as you'd like. Pull requests are welcome.

## License
TagesschauScraper is licensed under the GPL-3.0 license.


## Disclaimer
Please note that this is a scraping tool, and using it to scrape website data without the website owner's consent may be against their terms of service. Use at your own risk.
