import os
import numpy as np
from pathlib import Path
import pandas as pd
from io import StringIO
import boto3
from sensorFaultDetection.utils import get_size
from sensorFaultDetection.logger import logging
from sklearn.model_selection import train_test_split
from sensorFaultDetection.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.client = boto3.client('s3',
                      aws_access_key_id=self.config.s3_key,
                      aws_secret_access_key=self.config.s3_secret_key
                      )


    def dowload_file(self):
        if not os.path.exists(self.config.local_data_file):
            csv_obj = self.client.get_object(Bucket=self.config.s3_bucket, Key=self.config.object_key)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_string))
            
            if "_id" in list(df):
                df = df.drop('_id', axis=1)
            df.replace({'na': np.nan}, inplace=True)
            df.drop(columns= self.config.drop_columns, axis=1, inplace=True)

            df.to_csv(self.config.local_data_file, index=False, header=True)
            logging.info(f'{self.config.local_data_file} is downloaded!') 
            self.df = df             

        else:
            logging.info(f"File already exists of size : {get_size(Path(self.config.local_data_file))}")

    def train_test_creation(self):
        df = pd.read_csv(self.config.local_data_file)
        target_feature  = 'class'
        y = df[target_feature]
        X = df.drop(target_feature, axis=1)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.config.train_test_ratio, shuffle=True)
        X_train[target_feature] = y_train
        X_test[target_feature] = y_test

        # shift column 'C' to first position
        first_column_train = X_train.pop(target_feature) 
        first_column_test = X_test.pop(target_feature)   
        # insert column using insert(position,column_name,first_column) function
        X_train.insert(0, target_feature, first_column_train)
        X_test.insert(0, target_feature, first_column_test)

        X_train.to_csv(self.config.train_data_file, index=False, header=True)
        logging.info(f'Train data is created and saved at {self.config.train_data_file}!')   
        X_test.to_csv(self.config.test_data_file, index=False, header=True)
        logging.info(f'Test data is created and saved at {self.config.test_data_file}!')   