# TagesschauScraper

A library for scraping the German news archive of Tagesschau.de

## Usage

Here's an example of how to use the library to scrape teaser info from the Tagesschau archive:

```python
import os
from datetime import date
from tagesschauscraper import constants, helper, tagesschau

# Scraping teaser published on <date_> and in specific news category  
date_ = date(2022,3,1)
category = "wirtschaft"

# Initialize scraper, create url and run
tagesschauScraper = tagesschau.TagesschauScraper()
url = tagesschau.create_url_for_news_archive(date_, category=category)
teaser = tagesschauScraper.scrape_teaser(url)

# Save output in a hierarchical directory tree
dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(date_)
file_path = os.path.join(dateDirectoryTreeCreator.path, helper.create_file_name_from_date(date_, extension='.json'))
helper.save_to_json(teaser, file_path)
```
The result saved in json format looks the following (only a snippet):
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
