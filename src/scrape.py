import importlib
import json

def run_scrapers():
    scrapers = [
        'trading212',
    ]
    for scraper_name in scrapers:
        module = importlib.import_module('scrapers.' + scraper_name)
        scraper = getattr(module, 'scrape')

        print(f"Running scraper {scraper_name}...")

        print(f"   Scraping...")
        data = scraper()

        print(f"   Saving result...")
        with open('./data/' + scraper_name + '.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    run_scrapers()