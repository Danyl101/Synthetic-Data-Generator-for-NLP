from sentence_transformers import SentenceTransformer, util
import os
from config_loader import config
import logging_loader
import logging

logger=logging.getLogger("Bert_Semantic")

from .utils import text_acquire,text_encoding


model = SentenceTransformer("all-MiniLM-L6-v2")

content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['cleaned_text_data'])

paraphrased_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['paraphrased_text_data'])

def compute_bert_similarity(text, paraphrased_text,filename):
    results=[]
    for fname,chunk,paraphrased_chunk in zip(text,paraphrased_text,filename):
        for embedding,paraphrased_embedding in zip(chunk,paraphrased_chunk):
            embeddings1 = model.encode(embedding, convert_to_tensor=True)
            embeddings2 = model.encode(paraphrased_embedding, convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2).item()
            results.append({"file": fname,
                    "original": embedding,
                    "paraphrase": paraphrased_embedding,
                    "similarity": cosine_scores
                })
            logger.info(f"Computed similarity for {fname}")
    return results

def remove_files(result,path):
    for i in result:
        if i["similarity"]<0.3 or i["similarity"]>0.9:
            os.remove(os.path.join(path,i["file"]))
            logger.info(f"Removed {i['file']} due to similarity score of {i['similarity']}")
        
def run():
    texts,filename=text_acquire(content_dir)
    encoding=text_encoding(texts)
    paraphrased_texts,paraphrased_filename=text_acquire(paraphrased_dir)
    paraphrased_encoding=text_encoding(paraphrased_texts)
    result=compute_bert_similarity(encoding,paraphrased_encoding,filename)
    remove_files(result,paraphrased_dir)
    
    




