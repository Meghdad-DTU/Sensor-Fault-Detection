
import os
import datetime
import sys
import numpy as np
import pandas as pd
import shutil
from sensorFaultDetection. logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.utils import load_pickle, save_pickle, classifier_performance_report, write_yaml_file
from sensorFaultDetection.entity.config_entity import ModelEvaluationConfig


class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))


class ModelResolver:
    def __init__(self, trained_model_dir, best_model_dir):
        self.trained_model_dir = trained_model_dir
        self.best_model_dir = best_model_dir

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

    @staticmethod
    def sort_dates(dates):
        # Define a key function that converts a date string to a datetime object
        def date_key(date_string):
            return datetime.datetime.strptime(date_string, '%Y-%m-%d_%H-%M-%S')
             
        # Use the sorted function to sort the list of dates, using the date_key function as the key
        return sorted(dates, key=date_key)


    def get_latest_model_path(self, model_dir) -> str:
        try:            
            timestamps = self.only_directory_names(model_dir)            
            sorted_timestamps = self.sort_dates(timestamps)                             
            latest_timestamps = sorted_timestamps[-1]
            latest_model_path = os.path.join(model_dir, latest_timestamps, 'model.pkl')            
            return latest_model_path
        except Exception as e:
            raise CustomException(e, sys)
        
    def is_model_exists(self) -> bool:
        try:
            if self.is_dir_empty(self.trained_model_dir) is False:                              
                return False
            
            latest_model_path = self.get_latest_model_path(self.trained_model_dir)           
            if not os.path.exists(latest_model_path):                
                return False
            
            if self.is_dir_empty(self.best_model_dir) is False:                
                timestamps = os.listdir(self.trained_model_dir)
                sorted_timestamps = self.sort_dates(timestamps)            
                latest_timestamps = sorted_timestamps[-1]
                source_file = os.path.join(self.trained_model_dir, latest_timestamps, 'model.pkl')
                destination_file = os.path.join(self.best_model_dir, latest_timestamps)
                os.makedirs(destination_file, exist_ok= True)
                shutil.copy (source_file, destination_file) 
                logging.info(f'There was no best model. Hence, a new best model saved to {destination_file}!')           
            
            best_model_path = self.get_latest_model_path(self.best_model_dir)            
            if not os.path.exists(best_model_path):                              
                return False            
            
            return True
        
        except Exception as e:
            CustomException(e, sys)

            
class ModelEvaluation:
    is_model_accepted = False
    
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_model_evaluation(self) -> None:
        try:
            # valid train and test file dataframes
            train_dataframe = self.read_data(self.config.valid_train_file)
            logging.info(f"Train data is read from {self.config.valid_train_file}!")
            test_dataframe = self.read_data(self.config.valid_test_file)
            logging.info(f"Test data is read from {self.config.valid_test_file}!")

            # calculate model performance on whole dataframe
            df = pd.concat([train_dataframe, test_dataframe])
            input_feature_df = df.drop(columns=self.config.target_column, axis=1)
            target_feature_df = df[self.config.target_column]
            target_feature_df = target_feature_df.replace(TargetValueMapping().to_dict())

            # loading_trained model
            model_resolver = ModelResolver(self.config.trained_model_path, self.config.root_dir)
            status = model_resolver.is_model_exists()
            if not status:
                return logging.info("WARNING: There is no trained model path available!")                
          
            latest_model_path = model_resolver.get_latest_model_path(self.config.trained_model_path)            
            latest_model = load_pickle(latest_model_path)           
            best_model_path = model_resolver.get_latest_model_path(self.config.root_dir)            
            best_model = load_pickle(best_model_path)

            y_true = np.array(target_feature_df)
            y_best_pred = best_model.predict(input_feature_df)
            y_latest_pred = latest_model.predict(input_feature_df)
            labels = ["Negative", "Positive"]
            
            best_metric_table= classifier_performance_report(
                y_true= y_true,
                y_pred= y_best_pred, 
                path= None, 
                classes=labels
                )
            logging.info(f"Model performance metrics for best model is completed!")
            
            
            latest_metric_table = classifier_performance_report(
                y_true= y_true, 
                y_pred= y_latest_pred, 
                path= None, 
                classes=labels
                )
            logging.info(f"Model performance metrics for latest model is completed!")

            improved_accuracy = latest_metric_table['f1-score'].values[-1] - best_metric_table['f1-score'].values[-1]            
            
            if improved_accuracy > self.config.model_evaluation_changed_threshold:  
                ModelEvaluation.is_model_accepted = True              
                logging.info(f"Latest model performs better than the old version!")                
                best_metric_table= classifier_performance_report(
                    y_true= y_true,
                    y_pred= y_best_pred, 
                    path= os.path.join(os.path.dirname(best_model_path, 'performance_metrics.csv')),
                    classes=labels
                )


                new_best_model_path = os.path.join(os.path.dirname(best_model_path, 'model.pkl'))
                # save the best model in both artifacts and save_model folders
                save_pickle(path= new_best_model_path, obj= latest_model)
                save_pickle(path= self.config.saved_model_path, obj= latest_model)
                logging.info(f"Best model is replaced by a new vesion!") 

            else:                
                if not os.path.exists(self.config.saved_model_path):
                    save_pickle(path= self.config.saved_model_path, obj= best_model)
                logging.info(f"Latest model does not perform better than the old version!")                

            evaluation_report = dict()
            evaluation_report['is_model_accepted'] = ModelEvaluation.is_model_accepted
            evaluation_report['improved_accuracy']= float(improved_accuracy)
            evaluation_report['best_model_path']=  best_model_path
            evaluation_report['latest_model_path']=  latest_model_path

            write_yaml_file(path= self.config.evaluation_report_file, content= evaluation_report, replace= True)

        except Exception as e:
            raise CustomException(e, sys)
    
    
    
    