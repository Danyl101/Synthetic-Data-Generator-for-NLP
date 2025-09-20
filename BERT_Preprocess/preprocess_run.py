from .Clean_run import run_clean
from .paraphraser import run_paraphrasing
from .bert_semantic import run_semantic_comparison

if __name__=="__main__":
    run_clean()
    run_paraphrasing()
    run_semantic_comparison()
    