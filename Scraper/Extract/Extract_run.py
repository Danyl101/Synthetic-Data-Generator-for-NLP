import json
import os
import logging_loader
import logging

logger=logging.getLogger("Extract")


from config_loader import config

from .content_extract import extract_multiple_articles

def extract_run():
    with open(config['paths']['scraping']['scraped_links'], 'r' ,encoding="utf-8",errors="replace") as f: #Loads json file 
        article = json.load(f) 
        json_dict=article["articles"] #articles is dictionary inside the json file ,this loads the actual articles into json_dict
    os.makedirs(config['paths']['bert']['raw_text_data']['raw_data_folder'], exist_ok=True)  # Ensure directory exists

    extracted_articles = extract_multiple_articles(json_dict, max_scrolls=10) #Calls the complete extraction process
    logger.info(f"Total Extracted articles:{len(extracted_articles)}")
    
if __name__=="__main__":
    extract_run()
    
    
    
    
    
        
    
    

