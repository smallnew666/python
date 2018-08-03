from instagram_scraper import instagram_scraper

for url, caption, hashtags, mentions in scrape_instagram(['quotes', 'meet'], 5):
    print(url, caption, hashtags, mentions)