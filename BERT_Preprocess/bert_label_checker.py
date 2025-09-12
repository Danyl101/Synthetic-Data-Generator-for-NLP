import os
import csv
import shutil
from config_loader import config

original_csv=config['paths']['bert']['labels']['original_data_csv_label']

paraphrased_csv=config['paths']['bert']['labels']['paraphrased_data_csv_label']

content_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['cleaned_data_folder'])

os.makedirs(config['paths']['bert']['raw_text_data']['paraphrased_data_folder'],exist_ok=True)

paraphrased_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',config['paths']['bert']['raw_text_data']['paraphrased_data_folder'])

def label_check(csv_path):
    with open(csv_path,"r",encoding="utf-8",errors="replace")as csvfile:
        reader=csv.reader(csvfile)
        header=next(reader)
        label=[]
        for row in reader:
            if(row[1]=="positive"):
                label.append((row[0], row[1]))
    return label

def content_check(original_dict,paraphrased_dict):
    final_label=[]
    for original_name, original_label in original_dict:
        for paraphrased_name ,paraphrased_label in paraphrased_dict:
            if original_name == paraphrased_name:
                print("success 2")
                if original_label == paraphrased_label:
                    name_only, ext = os.path.splitext(paraphrased_name)
                    changed_filename = name_only + "_paraphrased.txt"
                    final_label.append((changed_filename,paraphrased_label))
                    print("✅ Text renamed:", changed_filename)
                    
                    src = os.path.join(content_dir, original_name)
                    dst = os.path.join(paraphrased_dir, changed_filename)

                    # move (or copy) file
                    if os.path.exists(src):
                        shutil.move(src, dst)   # use shutil.copy(src, dst) if you want to keep original
                        print("✅ File moved:", dst)
    return final_label
                    
    
original_label=label_check(original_csv)
print(original_label)

paraphrased_label=label_check(paraphrased_csv)
print(paraphrased_label)

results=content_check(original_label,paraphrased_label)




    
            
