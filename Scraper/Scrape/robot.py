import requests
import urllib.robotparser
from urllib.parse import urlparse
import logging

logger=logging.getLogger("Scraper")

def fetch_robots_txt(site):
    try:
        resp = requests.get(site + "/robots.txt", timeout=10)
        return resp.text
    except:
        return None
    
def can_scrape(url, user_agent='*'):
    try:
        # Extract domain
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Construct robots.txt URL
        robots_url = f"{base_url}/robots.txt"

        # Read and parse robots.txt
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()

        # Check if allowed
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logger.error(f"[WARN] Could not parse robots.txt for {url}: {e}")
        # Assume allowed if robots.txt is unreachable
        return True