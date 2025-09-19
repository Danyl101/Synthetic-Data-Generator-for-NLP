import logging
import traceback
import os
import csv
from config_loader import config

#Checks whether the files have text for each function
def pipeline(text,funcs):
    for func in funcs:
        text=func(text)
        if text is None:
            return None
    return text

#Function to save files
def save_file(filename, full_content,path,suffix=""):
    try:
        if not full_content.strip(): #Checks if there is content
            logging.info(f"No content found for: {filename}")
            return False
    except Exception as e:
        logging.error(f"Content cleaning failed : {e}")
        logging.debug(traceback.format_exc())
        return False

    try:
        if not filename:
            logging.warning(f"Sanitized filename is empty for title: {filename}")
            return False
        name,ext=os.path.splitext(filename)
        filename=f"{name}{suffix}{ext}"if suffix else filename

        os.makedirs(path, exist_ok=True)

        filepath = os.path.join(path, filename) #Creates a file in the necessary folder 
        with open(filepath, "w", encoding="utf-8") as f: #Opens created file 
            f.write(full_content) #Writes content into it

        logging.info(f"Saved: {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving file {filename} : {e}")
        logging.debug(traceback.format_exc())
        return False
    

def text_acquire(dir):
    all_text=[]
    all_filename=[]
    for filename in os.listdir(dir): #Acquires files in directory
        logging.info("Found file: {}".format(filename))
        filepath=os.path.join(dir,filename) #Sets filepath
        with open(filepath,"r",encoding="utf-8")as f:
            text=f.read()
            all_text.append(text) #Appends full text
            all_filename.append(filename) #Appends filename
            logging.info("File read successfully: {}".format(filename))
    return all_text,all_filename
    
def text_encoding(texts,max_text=450,step=350):
    all_text=[]
    for text in texts:
        all_snippets=[]
        for start_idx in range(0,len(text),step):
            text_snippet=text[start_idx:start_idx+max_text] #Breaks down full text into small chunks
            all_snippets.append(text_snippet) #Appends small chunks into list
        all_text.append(all_snippets)
    return all_text

