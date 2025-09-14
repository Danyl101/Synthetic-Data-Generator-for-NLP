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
def save_file(filename, full_content):
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
        filename = filename[:] # leave room for .txt

        os.makedirs(config['paths']['bert']['raw_text_data']['cleaned_data_folder'], exist_ok=True)

        filepath = os.path.join(config['paths']['bert']['raw_text_data']['cleaned_data_folder'], filename) #Creates a file in the necessary folder 
        with open(filepath, "w", encoding="utf-8") as f: #Opens created file 
            f.write(full_content) #Writes content into it

        logging.info(f"Saved: {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving file {filename} : {e}")
        logging.debug(traceback.format_exc())
        return False


def label_acquire():
    labels=[]
    filename_label={}
    with open(config['paths']['bert']['labels']['original_label'],"r",encoding="utf-8",errors="replace")as csvfile:
        reader=csv.reader(csvfile)
        header=next(reader)
        for row in reader:
            labels.append(row[1])
            filename_label[row[0]]=row[1]
    return labels,filename_label

def text_acquire(filename_label):
    content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',
                             config['paths']['bert']['raw_text_data']['cleaned_data_folder'])
    all_text=[]
    all_filename=[]
    for filename in os.listdir(content_dir):
        print("1")
        if filename_label.get(filename) == "positive":
            print("2")
            filepath=os.path.join(content_dir,filename)
            with open(filepath,"r",encoding="utf-8")as f:
                text=f.read()
                all_text.append(text)
                all_filename.append(filename)
    return all_text,all_filename