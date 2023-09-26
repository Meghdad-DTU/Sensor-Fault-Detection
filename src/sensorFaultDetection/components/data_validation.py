import sys
import pandas as pd
from sensorFaultDetection.utils import write_yaml_file
from scipy.stats import ks_2samp
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.logger import logging
from sensorFaultDetection.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.config.schema_columns)                        
            if len(list(dataframe))==number_of_columns:
                return True
            else:
                logging.info('WARNING: Required number of columns is differnt from dataframe columns!')
                return False
        except Exception as e:
            raise CustomException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self.config.schema_numerical_columns
            dataframe_columns = list(dataframe)

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column  not in dataframe_columns:
                    numerical_column_present= False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f'Missing numerical columns: {missing_numerical_columns}')
            return numerical_column_present
        except Exception as e:
            CustomException(e, sys)

    def drop_zero_std_columns(self, dataframe: pd.DataFrame):
        pass  

    @staticmethod
    def detect_dataset_drift(base_dataframe: pd.DataFrame, current_datafrme: pd.DataFrame, threshold: float):
        try:
            status = True
            report ={}
            for column in base_dataframe.columns:
                df1 = base_dataframe[column]
                df2 = current_datafrme[column]
                is_same_dist = ks_2samp(df1, df2)
                if is_same_dist.pvalue >= threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({column:{
                    'p_value': float(is_same_dist.pvalue),
                    'drift_status': is_found
                            }})
            return status, report
        except Exception as e:
            raise CustomException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    
    def initiate_data_validation(self):
        error_message = ""

        train_dataframe = self.read_data(self.config.train_data_file)
        logging.info(f"Train data is read from {self.config.train_data_file}!") 
        test_dataframe = self.read_data(self.config.test_data_file)
        logging.info(f"Test data is read from {self.config.test_data_file}!") 

        status= self.validate_number_of_columns(dataframe= train_dataframe)        
        if not status:
            error_message = f'{error_message} Train dataframe does not contain all columns!'
        
        status = self.validate_number_of_columns(dataframe= test_dataframe)       
        if not status:
            error_message = f'{error_message} Test dataframe does not contain all columns!'

        status = self.is_numerical_column_exist(dataframe= train_dataframe)
        if not status:
            error_message = f'{error_message} Train dataframe does not contain all numerical columns!'

        status = self.is_numerical_column_exist(dataframe= test_dataframe)
        if not status:
            error_message = f'{error_message} Test dataframe does not contain all numerical columns!'

        
        if len(error_message)>0:
            raise Exception(error_message)        
        
        #############################################################################################
        # Data drift check at traing model stage
        # Here, we need to test whether test datset and train dataset are from same distribution i.e. identical
        # Base dataset: Train
        # To compare with: Test
        # If same distribution: No drift
        # Solution: If NOT then do train split correctly

        # Data drift at prediction stage:
        # NOT possible to detect data drift immediately as it is NOT possible to summerize one record
        # Solution: Saving each request in database and then fetching all request by hour or day 
        # Base dataset: Train
        # To compare with: Collected data, batch data
        # If huge differnce, go for retraining

        # Concept drift:
        # It related to model where relation between input feature and target feature is changed.
        # Solution: Retrain the model

        # Target drift:
        # If the distribution of target column changed e.g., having a new category in the target variable
        # Solution: Retrain the model
        #############################################################################################

        status, drift_report = self.detect_dataset_drift(train_dataframe, test_dataframe, self.config.pvalue_threshold)
        if status:   
            logging.info('NO data drift issue!')         
            train_dataframe.to_csv(self.config.valid_train_file, index=False, header=True)
            test_dataframe.to_csv(self.config.valid_test_file, index=False, header=True)
            logging.info(f'Train set is saved at {self.config.valid_train_file}!') 
            logging.info(f'Test set is saved at {self.config.valid_test_file}!')   
        else:
            logging.info('WARNING: We faced data drift issue, check report.yaml!')
            train_dataframe.to_csv(self.config.invalid_train_file, index=False, header=True)
            test_dataframe.to_csv(self.config.invalid_test_file, index=False, header=True)
            logging.info(f'Train set is saved at {self.config.invalid_train_file}!') 
            logging.info(f'Test set is saved at {self.config.invalid_test_file}!') 


        write_yaml_file(path= self.config.drift_report_file, content= drift_report, replace= True)