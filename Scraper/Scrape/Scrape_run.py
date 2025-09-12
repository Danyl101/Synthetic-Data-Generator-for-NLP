from .link_extract import scrape_multiple_sites
from .utils import websites,goodlist
import logging_loader
import logging

logger=logging.getLogger("Scraper")

def run_scrape():
    print(websites)
    print(goodlist)
    cleaned_articles = scrape_multiple_sites(websites, max_scrolls=15)
    logger.info(f"Total articles scraped: {len(cleaned_articles)}") #Returns no of articles that are available after cleaning
    
if __name__ == "__main__":
    run_scrape()
    
   