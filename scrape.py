from scraping.tagesschau import TagesschauDB
from scraping.tagesschau import TagesschauScraper
from scraping.tagesschau import get_dates_in_interval
from scraping.retrieve import get_soup
import requests
from datetime import date
from tqdm import tqdm
import pandas as pd

def main():
    db = TagesschauDB()
    # db.drop_table()
    # db.create_table()
    
    tagesschauScraper = TagesschauScraper()
    dates = pd.date_range('2020-01-01', '2020-01-10', freq='D')
    
    for date_ in tqdm(dates):
        url = tagesschauScraper.get_url(date_)
        print(url)
        response = requests.get(url)
        soup = get_soup(response)
        teasers = tagesschauScraper.get_all_news_teaser(soup)
        for teaser in teasers:
            if teaser:
                db.insert(teaser)
    
    

if __name__ == '__main__':
    main()