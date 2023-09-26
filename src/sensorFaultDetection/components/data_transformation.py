import sys
import pandas as pd
import numpy as np
from sensorFaultDetection.utils import save_pickle, save_numpy_array
from sensorFaultDetection.logger import logging
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.entity.config_entity import DataTransformationConfig



class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config       

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:       
            pipeline = Pipeline(
                steps=[                          
                    ('Imputer', SimpleImputer(strategy='constant', fill_value=0)), # replace missing values with zero
                    ('RobustScaler', RobustScaler())] # keep every feature in same range and handle ouliers
                    )     

            logging.info(f'Data transformer pipeline is created!')        
            return pipeline
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self):
        try:
            train_df = self.read_data(self.config.train_data_file)
            logging.info(f"Train data is read from {self.config.train_data_file}!")
            test_df = self.read_data(self.config.test_data_file)        
            logging.info(f"Test data is read from {self.config.test_data_file}!")             
            
            # train dataset
            input_feature_train_df = train_df.drop(columns=self.config.target_column, axis=1)
            target_feature_train_df = train_df[self.config.target_column]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            
            # test dataset
            input_feature_test_df = test_df.drop(columns=self.config.target_column, axis=1)
            target_feature_test_df = test_df[self.config.target_column]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())              

            logging.info(f"Applying preprocessing object on both train and test dataframes")
            preprocessor_obj = self.get_data_transformer_object()
            
            transformed_input_train_feature = preprocessor_obj.fit_transform(input_feature_train_df)       
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)                

            smt = SMOTETomek(sampling_strategy='minority')  
            logging.info(f"Applying data balancer object on both train and test data")         

            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_test_feature, target_feature_test_df)            

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            save_numpy_array(path=self.config.train_npy_file, array=train_arr )
            save_numpy_array(path=self.config.test_npy_file, array=test_arr)                            
            save_pickle(path= self.config.preprocessor_file, obj= preprocessor_obj)
        
        except Exception as e:
            raise CustomException(e, sys)

        