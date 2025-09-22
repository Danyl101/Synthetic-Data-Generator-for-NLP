from .Clean_run import run_clean
from .paraphraser import run_paraphrasing
from .bert_semantic import run_semantic_comparison

def preprocess_run():
    run_clean()
    run_paraphrasing()
    run_semantic_comparison()

if __name__=="__main__":
    preprocess_run()
    
    