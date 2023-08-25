# Old design
1. Create config for scraper
2. Initialize scraper: tagesschau.TagesschauScraper()
3. tagesschauScraper.get_news_from_archive(config)

# New design
1. Create config for scraper
2. Initialize TagesschauScraper with config
3. Execute TagesschauScraper, something like TagesschauScraper.scrape()