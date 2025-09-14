import torch
import pandas as pd
from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn as nn
import numpy as np
import os
import csv
import traceback
import torch.nn.functional as F

import logging_loader
import logging
from config_loader import config

logger=logging.getLogger("Bert_Label")

torch.manual_seed(42) #Sets seed to reduce randomness

device="cuda" if torch.cuda.is_available() else "cpu"

class_names=["negative","neutral","positive"] #Defines the sentiment classes
    
def text_encoding(texts,max_text=450,step=350):
    all_text=[]
    for text in texts:
        all_snippets=[]
        for start_idx in range(0,len(text),step):
            text_snippet=text[start_idx:start_idx+max_text]
            all_snippets.append(text_snippet)
        all_text.append(all_snippets)
    return all_text


def logits_pass(encodings): #Function to calculate sentiment of a text chunk
    try:
        agg_logits=None
        with torch.no_grad(): 
            for enc in encodings:
                input_ids=enc['input_ids'].to(device) #Moves encoded inputs into device
                attention_mask=enc['attention_mask'].to(device) #Moves encoded attention to device
                output=model(input_ids=input_ids,attention_mask=attention_mask) #Defines the above parameters into model
                logits=output.logits.squeeze(1) #Removes all dimensions of size 1 from logits 
                if agg_logits==None:
                    agglogits=logits #Adds logits initially
                else:
                    agg_logits=agg_logits+logits #Sumises logits 
                    
        probs=F.softmax(agg_logits,dim=1) #Converts logits into probability by quantifying with softmax
        pred_idx=torch.argmax(probs).item() #Returns the max sentiment value from chunk alongside its index
        return class_names[pred_idx], probs.cpu().numpy() #Returns the index and the probability
    except Exception as e:
        logger.error("Execution failed at logits pass")
        logger.error(traceback.format_exc())   

def max_pooling(probs):
    try:
        max_vals,_=torch.max(probs,dim=0)
        
        predicted_class_probs=torch.argmax(max_vals).item()
        
        predicted_label_probs = class_names[predicted_class_probs]
        logger.info("Average pooling execution successful")
    except Exception as e:
        logger.error("Execution failed at average pooling")
        logger.error(traceback.format_exc())

    return predicted_label_probs

def label_to_csv(filepath,label,content_dir,output_csv): #Saves the textfile and its corresponding sentiment to csv
    try:
        with open(output_csv,"a",newline='')as csvfile: 
            writer=csv.writer(csvfile) 
            writer.writerow([filepath,label])  #Writes the data into csv row
        logger.info("CSV writing")
    except Exception as e:
        logger.error("Execution failed at writing into csv")
        logger.error(traceback.format_exc())

def label_extract(Directory_name,csvpath):
    content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',Directory_name) #Acquires folder containing all extracted txt files
    for filepath in os.listdir(content_dir): 
        fullpath=os.path.join(content_dir,filepath) #Finds the path of the files
        if fullpath.endswith('txt'):
            with open(fullpath,"r",encoding='utf-8')as f:
                text=f.read()  #Reads the text file
                encoded=text_encoding(text) #Breaks text into chunks and encodes them
                label,probs=logits_pass(encoded) #Acquires the sentiment and its probability
                out=label_to_csv(filepath,label,content_dir,csvpath)
                print(probs) 
                print(label)     
                
def run_bert_label():
    paraphrased_path=config['paths']['bert']['raw_text_data']['paraphrased_data_folder']
    original_path=config['paths']['bert']['raw_text_data']['cleaned_data_folder']
    paraphrased_csv_path=config['paths']['bert']['labels']['paraphrased_label']
    original_csv_path=config['paths']['bert']['labels']['original_label']
    label_extract(paraphrased_path,paraphrased_csv_path)    
                
# Example usage:
if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone") #Loads tokenizer from pretrained finbert
    model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone") #Loads finbert for classification
    model.to(device)
    model.eval()
    run_bert_label()

        
        
