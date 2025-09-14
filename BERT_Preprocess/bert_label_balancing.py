from collections import Counter
import os
import csv
import torch
import transformers
from torch.nn import CrossEntropyLoss
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import logging_loader
import logging
from config_loader import config

logger=logging.getLogger("Bert_Label_Balancing")

device="cuda" if torch.cuda.is_available() else "cpu"

pegasus_model_name = config['paths']['model']['bert']['pretrained']['pegasus']

pegasus_tokenizer=PegasusTokenizer.from_pretrained(pegasus_model_name)
pegasus_model=PegasusForConditionalGeneration.from_pretrained(pegasus_model_name).to(device)

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
        if filename_label.get(filename) == "positive":
            logger.info("Found positive file: {}".format(filename))
            filepath=os.path.join(content_dir,filename)
            with open(filepath,"r",encoding="utf-8")as f:
                text=f.read()
                all_text.append(text)
                all_filename.append(filename)
                logger.info("File read successfully: {}".format(filename))
    return all_text,all_filename
    
def text_encoding(texts,max_text=450,step=350):
    all_text=[]
    for text in texts:
        all_snippets=[]
        for start_idx in range(0,len(text),step):
            text_snippet=text[start_idx:start_idx+max_text]
            all_snippets.append(text_snippet)
        all_text.append(all_snippets)
    return all_text

def translate(texts,num_return_sequences=2, num_beams=5):
    backtranslated_chunks = []
    for text in texts:
        single_page_text=[]
        for chunk in text:
            enc = pegasus_tokenizer(chunk,truncation=True,padding=True,max_length=512,return_tensors="pt")
            print(pegasus_model.config.max_position_embeddings)
            enc = {k: v.to(device) for k, v in enc.items()}
            outputs = pegasus_model.generate(**enc,max_length=512,num_beams=num_beams,num_return_sequences=num_return_sequences )
            paraphrased = pegasus_tokenizer.batch_decode(outputs, skip_special_tokens=True)
            single_page_text.append(paraphrased)
        backtranslated_chunks.append(single_page_text)
    return backtranslated_chunks

def save_file(content,filename):
    for text,name in zip(content,filename):
        full_text = " ".join([item for sublist in text for item in sublist])
        filepath=os.path.join(config['paths']['bert']['raw_text_data']['paraphrased_data_folder'],name)
        with open(filepath, "w",encoding="utf-8")as f:
            f.write(full_text)
            logger.info("File saved successfully: {}".format(name))

def run_bert_balancing():
    labels,filename_label=label_acquire()
    texts,filename=text_acquire(filename_label)
    encoding=text_encoding(texts)
    translated=translate(encoding)
    save_file(translated,filename)

if __name__=="__main__":
    run_bert_balancing()
    


    

    
        