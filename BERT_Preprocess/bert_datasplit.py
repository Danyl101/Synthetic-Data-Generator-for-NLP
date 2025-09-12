import os 
import shutil
import random
from config_loader import config

def datasplit():
    content_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',
                                config['paths']['bert']['raw_text_data']['cleaned_data_folder'])
    
    base_dir='Datasets'
    os.makedirs(base_dir,exist_ok=True)
    
    # Create these folders if they don't exist
    for folder in ['train_folder', 'val_folder', 'test_folder']:
        path=os.path.join(base_dir,folder)
        os.makedirs(path,exist_ok=True)
    
    filelist=[f for f in os.listdir(content_folder) if f.endswith('txt')]
    random.shuffle(filelist)
    
    total=len(filelist)
    train_end=int(total*0.6)
    val_end=int(total*0.2)+train_end
    
    train_files=filelist[:train_end]
    val_files=filelist[train_end:val_end]
    test_files=filelist[val_end:]
    
    for f in train_files:
        shutil.copy(os.path.join(config['paths']['bert']['raw_text_data']['cleaned_data_folder'],f),
                    os.path.join(config['paths']['bert']['model_data']['train_data_folder'],f))
        
    for f in val_files:
        shutil.copy(os.path.join(config['paths']['bert']['raw_text_data']['cleaned_data_folder'],f),
                    os.path.join(config['paths']['bert']['model_data']['validation_data_folder'],f))
        
    for f in test_files:
        shutil.copy(os.path.join(config['paths']['bert']['raw_text_data']['cleaned_data_folder'],f),
                    os.path.join(config['paths']['bert']['model_data']['test_data_folder'],f))
        
    print(total)
    print(len(train_files))
    print(len(val_files))
    print(len(test_files))
    
if __name__=="__main__":
    datasplit()
        
    
    
            
            
        
        
    
    