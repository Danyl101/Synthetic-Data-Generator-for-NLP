from .Clean_run import run_clean
from .bert_label import run_bert_label
from .bert_label_checker import run_label_check
from .bert_label_balancing import run_bert_balancing
from .bert_datasplit import datasplit

if __name__=="__main__":
    run_clean()
    run_bert_label()
    run_label_check()
    run_bert_balancing()
    datasplit()
    