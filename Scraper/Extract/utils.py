import logging
import re
import traceback
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from config_loader import config

logger=logging.getLogger("Extract")


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
}  #Mimics real browser request


def sanitize_filename(name):
    # Remove any character that's not alphanumeric, dash, underscore, or space
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace whitespace/newlines with underscore
    name = re.sub(r'[\s]+', '_', name)
    return name[:150] 
    
def save_file(title, full_content):
    try:
        if not  full_content.strip():
            logger.info(f"No content found for: {title}") #Log message
            logger.debug(traceback.format_exc())
            return None
    except Exception as e:
        logger.error(f"Content cleaning failed : {e}")
        logger.debug(traceback.format_exc())

    try:
        # Save as .txt file
        filename = sanitize_filename(title) + ".txt" #Cleans file names
        filepath = os.path.join(config['paths']['bert']['raw_text_data']['raw_data_folder'], filename) #Creates filepath for the files
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content) #Writes content to the file

        logger.info(f"Saved: {filename}") #Log message
        return full_content
    except Exception as e:
        logger.error(f"Error saving file {filename} :{e}")


def setup_driver(): #Setup Chrome WebDriver
    chrome_options=Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox") # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options) #Creates web driver instance

def is_browser_alive(driver): #Checks if browser is still running
    try:
        driver.title
        return True
    except:
        logger.debug(traceback.format_exc())
        return False