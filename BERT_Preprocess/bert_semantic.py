from sentence_transformers import SentenceTransformer, util
import os
from config_loader import config
import logging_loader
import logging
from collections import defaultdict

logger=logging.getLogger("Bert_Semantic")

from .utils import text_acquire,text_encoding

model = SentenceTransformer("all-MiniLM-L6-v2")

content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['cleaned_data_folder'])  #Directory with text data

paraphrased_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['paraphrased_data_folder']) #Directory with paraphrased content

def compute_bert_similarity(text, paraphrased_text,filename):
    results=[]
    score_dict =defaultdict(list)
    for chunk,paraphrased_chunk,fname in zip(text,paraphrased_text,filename): #Accesses nested content 
        for embedding,paraphrased_embedding in zip(chunk,paraphrased_chunk):
            embeddings1 = model.encode(embedding, convert_to_tensor=True) #Embedding of raw text data
            embeddings2 = model.encode(paraphrased_embedding, convert_to_tensor=True) #Embedding of paraphrased data
            cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2).item() #Computes cosine similairty of embeddings
            score_dict[fname].append(cosine_scores)
        
    for fname, scores in score_dict.items():
        avg_score = sum(scores) / len(scores)
        results.append({"file": fname,
                "similarity": avg_score
            }) 
        logger.info(f"Computed similarity for {fname} and has similarity of {avg_score}")
    return results

def remove_files(result,path):
    for i in result:
        if i["similarity"]<0.3 or i["similarity"]>0.9:
            try:
                os.remove(os.path.join(path,i["file"]))
                logger.info(f"Removed {i['file']} due to similarity score of {i['similarity']}")
            except Exception as e:
                logger.error(f"Error removing {i['file']}: {e}")

def clean_chunks(chunks):
    return [c.strip() for c in chunks if c.strip() and len(c.strip().split()) > 40]  # keeps only non-empty chunks with at least 3 words

        
def run_semantic_comparison():
    texts,filename=text_acquire(content_dir)
    encoding=text_encoding(texts)
    paraphrased_texts,paraphrased_filename=text_acquire(paraphrased_dir)
    paraphrased_encoding=text_encoding(paraphrased_texts)
    result=compute_bert_similarity(encoding,paraphrased_encoding,paraphrased_filename)
    remove_files(result,paraphrased_dir)
    
if __name__=="__main__":
    run_semantic_comparison()
    
    




