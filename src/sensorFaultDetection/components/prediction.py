import sys
import os
import pandas as pd
from pathlib import Path
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.utils import load_pickle
from sensorFaultDetection.entity.config_entity import PredictionConfig

class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))


class Prediction:
    def __init__(self, filename: Path, config: PredictionConfig):
        self.config = config
        self.filename = filename
    
    @staticmethod
    def is_dir_empty(path):       
        if os.path.exists(path) and not os.path.isfile(path):  
            # Checking if the directory is empty or not
            if not os.listdir(path):
                #Empty directory
                return False
            else:
                return True
        else:
            #The path is either for a file or not valid"
            return False
    
    @staticmethod
    def only_directory_names(dir_path):
        # How to list ONLY directories in Python
        dir_names = []
        items = os.listdir(dir_path)        
        for item in items:
            if os.path.isdir(os.path.join(dir_path, item)):
                dir_names.append(item)
        return dir_names
    
    def get_best_model_path(self) -> Path:
        try:
            if self.is_dir_empty(self.config.best_model_dir) is False:                              
                raise Exception("WARNING: there is no trained model available for prediction!")      
                   
            dir_name = self.only_directory_names(self.config.best_model_dir)[-1]                      
            best_model_path = os.path.join(self.config.best_model_dir, dir_name, 'model.pkl')                     
            if not os.path.exists(best_model_path):                              
                raise Exception("WARNING:  there is no trained model available for prediction!")             
            
            return best_model_path
        
        except Exception as e:
            CustomException(e, sys)
    
    def initiate_prediction(self):
        try:
            best_model_path = self.get_best_model_path()            
            model = load_pickle(best_model_path)
            df = pd.read_csv(self.filename)
            input_variables = self.config.input_variables  

            if self.config.target_column in df.columns:
                df.drop(self.config.target_column, axis=1, inplace=True)                     
            
            column_present= True
            missing__columns = []
            for column in df.columns:
                if column  not in input_variables:
                    column_present= False
                    missing__columns.append(column)
            
            if not column_present:
                raise Exception(f"WARNING: missing column issue: {missing__columns}")
            
            df = df[input_variables]                                   
            logging.info("Reading data is completed!")
            y_pred = model.predict(df)
            df['predicted_class']= y_pred
            df['predicted_class'].replace(TargetValueMapping().reverse_mapping(), inplace=True)
            logging.info("Implementation of the trained model on the new data is completed!")            
            
            return df

        except Exception as e:
            raise CustomException(e, sys)