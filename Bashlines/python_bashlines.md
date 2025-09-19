
                            VIRTUAL ENVIRONMENT

python -m venv venv

venv\Scripts\activate

py -3.10 -m venv venv 

deactivate 

python -m pip install  
                (If pip is broken in venv)

python -m spacy download en_core_web_sm

Remove-Item -Recurse -Force venv

pip install -r requirements.txt

                            FLASK RUNNING

$env:PYTHONPATH = (Get-Location).Path
python -m frontend.src.api.flask_api.flask_run

                                SCRAPE

SCRAPER 

utils

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\Scraper\Scrape"
python -m Scraper.Scrape.utils

___________________________

scrape run

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\Scraper\Scrape"
>> python -m Scraper.Scrape.Scrape_run

___________________________

EXTRACT

utils.py

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\Scraper\Extract"
python -m Scraper.Extract.utils

Extract_run.py

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\Scraper\Extract"
>> python -m Scraper.Extract.Extract_run

                                    BiLSTM Preprocess

lstm_dataextract

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Preprocess"
python -m BiLSTM_Preprocess.lstm_dataextract

____________________________

lstm_dataprocess

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Preprocess"
python -m BiLSTM_Preprocess.lstm_dataprocess


                                    BiLSTM Model
                        
lstm dataload

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Model"     
python -m BiLSTM_Model.lstm_dataload

____________________________

lstm model

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Model"     
python -m BiLSTM_Model.lstm_model

____________________________

lstm utils

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Model"     
python -m BiLSTM_Model.lstm_utils

____________________________

lstm main

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BiLSTM_Model"     
python -m BiLSTM_Model.main   

                                BERT Preprocess

Preprocess

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.preprocess_run 

__________________________________

Clean run

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.Clean_run 

_________________________________

utils 

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.utils

_________________________________

bert datasplit

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.bert_datasplit

________________________________

paraphraser

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.paraphraser 

________________________________

bert semantic

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.bert_semantic

________________________________

bert label

$env:PYTHONPATH = "D:\Synthetic_Data_Generator\BERT_Preprocess"
python -m BERT_Preprocess.bert_label







        