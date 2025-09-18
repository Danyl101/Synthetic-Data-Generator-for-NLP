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

from .utils import text_acquire, text_encoding ,save_file

logger=logging.getLogger("Bert_Label_Balancing")

path=config['paths']['bert']['raw_text_data']['paraphrased_data_folder']

content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',
                             config['paths']['bert']['raw_text_data']['cleaned_data_folder'])

device="cuda" if torch.cuda.is_available() else "cpu"

pegasus_model_name = config['paths']['model']['bert']['pretrained']['pegasus']

pegasus_tokenizer=PegasusTokenizer.from_pretrained(pegasus_model_name)
pegasus_model=PegasusForConditionalGeneration.from_pretrained(pegasus_model_name).to(device)

def translate(texts, filenames, num_return_sequences=2, num_beams=5):
    all_results = {}  # collect results for all files
    for text, fname in zip(texts, filenames):
        paraphrases_for_file = {}  # collect all chunks for this file
        for chunk in text:
            enc = pegasus_tokenizer(
                chunk,truncation=True,padding=True,max_length=512,return_tensors="pt"
            )
            enc = {k: v.to(device) for k, v in enc.items()}

            outputs = pegasus_model.generate(
                **enc,max_length=512,num_beams=num_beams,num_return_sequences=num_return_sequences
            )
            paraphrased = pegasus_tokenizer.batch_decode(outputs, skip_special_tokens=True)

            paraphrases_for_file[chunk] = paraphrased
        all_results[fname] = paraphrases_for_file
        logger.info(f"Resulting Dict {all_results}")
        logger.info(f"Paraphrasing of {fname} successful")
    return all_results


def run_bert_balancing():
    texts,filename=text_acquire(content_dir)
    encoding=text_encoding(texts)
    translated=translate(encoding,filename)
    for fname,paraphrases in translated.items():
        for chunk,paraphrased_chunks in paraphrases.items():
            #for i,paraphrased_chunk in enumerate(paraphrased_chunks):
            save_file(fname,paraphrased_chunks,path,suffix=f"_paraphrased_")
        

if __name__=="__main__":
    run_bert_balancing()
    


    

    
        
        