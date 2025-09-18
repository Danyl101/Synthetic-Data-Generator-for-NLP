from .Clean_run import run_clean
from .paraphraser import run_bert_balancing
from .bert_datasplit import datasplit

if __name__=="__main__":
    run_clean()
    run_bert_balancing()
    datasplit()
    