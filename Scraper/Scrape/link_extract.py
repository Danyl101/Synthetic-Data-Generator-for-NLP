import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urlparse
from .utils import write_to_json,is_browser_alive,setup_driver,goodlist
from .robot import can_scrape

logger=logging.getLogger("Scraper")


def scroll_and_scrape(driver, url, max_scrolls=10):#Function to scroll and scrape articles from a given URL
    try:
        driver.get(url) 
    except TimeoutException: #Handles site timeouts 
        logger.error(f"Timeout while loading {url}, retrying...")
        return []
      
    time.sleep(3) #Wait for dyanmic content to load 

    last_height = driver.execute_script("return document.body.scrollHeight") #Gets Height of the page to scroll properly
    raw_articles =[]

    for _ in range(max_scrolls): #Function to Scroll through page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Scrolls through page
        time.sleep(2) #Waits for dynamic content to load 

        try:
            elems = driver.find_elements(By.TAG_NAME, 'a') #Acquires all anchor tags
            for elem in elems: #Iterates through elements 
                try:
                    link = elem.get_attribute('href') #Acquires link from these elements 
                    title = elem.text.strip() #Produces title from link
                    if link and title and len(title) > 20: # Filters out garbage links like javascript(0)
                        raw_articles.append((title.lower(), link.lower())) 
                except StaleElementReferenceException: #Handles stale DOM elements
                    continue        
        except Exception:
            logger.error("Error while fetching elements, retrying...")
            continue
            
        new_height = driver.execute_script("return document.body.scrollHeight") #Height of the scrolled page 
        if new_height == last_height: #Height of new scrolled page is same to previous page
            break
        last_height = new_height
    return clean_articles(raw_articles) #Calls clean articles function to filter out unwanted sites

def clean_articles(raw_articles): #Function to clean articles and filter out unwanted sites
    cleaned_articles = []
 
    for title, link in raw_articles: #Function to filter only good sites from the articles extracted 
        if any(good in link.lower() for good in goodlist):
            if(can_scrape(link)):
                cleaned_articles.append({
                    "title": title.lower(),
                    "link": link.lower()
            }) #Appends clean sites to final list 

    return write_to_json(cleaned_articles) #Calls write to json function to write articles to a json file
    
def scrape_multiple_sites(sites, max_scrolls=10): #Function to access multiple sites 
    driver = setup_driver() #Initializes web driver 
    all_data = []

    for site in sites:
        logger.info(f"Scraping {site}...")
        try:
            if not is_browser_alive(driver): #Checks if web driver is dead or alive
                driver.quit() #Deletes existing driver 
                driver = setup_driver() #Initializes new driver
            data = scroll_and_scrape(driver, site, max_scrolls=max_scrolls) #Calls scroll and scrape function
            all_data.extend(data)
        except Exception as e:
            logger.error(f"Error scraping {site}: {e}")
            continue

    driver.quit()
    return all_data