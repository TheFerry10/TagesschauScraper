import os
from datetime import date

from scraping import helper, tagesschau


def main():

    tagesschauScraper = tagesschau.TagesschauScraper()
    # dates = pd.date_range('2020-01-01', '2020-01-10', freq='D')
    # for date_ in tqdm(dates):

    date_ = date.today()
    url = tagesschau.create_url_for_news_archive(date_, ressort="wirtschaft")
    teaser = tagesschauScraper.scrape_teaser(url)
    
    dateDirectoryTreeCreator = helper.DateDirectoryTreeCreator(date_)
    file_path = dateDirectoryTreeCreator.get_file_path_name(extension='.json')
    helper.save_to_json(teaser, file_path)

if __name__ == "__main__":
    main()
