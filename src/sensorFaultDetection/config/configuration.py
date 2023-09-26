import os
from sensorFaultDetection.constants import *
from sensorFaultDetection.utils import read_yaml, create_directories
from sensorFaultDetection.entity.config_entity import (DataIngestionConfig,
                                                       DataValidationConfig,
                                                       DataTransformationConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 secret_filepath=SECRET_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH
                 ):
        
        self.config = read_yaml(config_filepath)
        self.secret = read_yaml(secret_filepath)
        self.schema = read_yaml(schema_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        secret = self.secret.aws_credential

        create_directories([config.ROOT_DIR])

        data_ingestion_config = DataIngestionConfig(
            root_dir= config.ROOT_DIR,
            s3_bucket= secret.S3_BUCKET,
            s3_key= secret.S3_KEY,
            s3_secret_key= secret.S3_SECRET_KEY,
            object_key= secret.OBJECT_KEY,
            local_data_file= config.LOCAL_DATA_FILE,
            train_test_ratio= self.params.TRAIN_TEST_RATIO,
            train_data_file= config.TRAIN_DATA_FILE,
            test_data_file= config.TEST_DATA_FILE,
            drop_columns= self.schema.drop_columns

        )        

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        valid_dir = os.path.dirname(config.VALID_TRAIN_FILE)
        invalid_dir = os.path.dirname(config.INVALID_TRAIN_FILE)
        report_dir = os.path.dirname(config.DRIFT_REPORT_FILE)

        create_directories([config.ROOT_DIR, valid_dir, invalid_dir, report_dir])

        data_validation_config = DataValidationConfig(
            root_dir= config.ROOT_DIR,
            train_data_file= self.config.data_ingestion.TRAIN_DATA_FILE,
            test_data_file= self.config.data_ingestion.TEST_DATA_FILE,
            valid_train_file= config.VALID_TRAIN_FILE,
            valid_test_file= config.VALID_TEST_FILE,
            invalid_train_file= config.INVALID_TRAIN_FILE,
            invalid_test_file= config.INVALID_TEST_FILE,
            drift_report_file= config.DRIFT_REPORT_FILE,
            schema_columns= self.schema.columns,
            schema_numerical_columns= self.schema.numerical_columns,            
            pvalue_threshold= self.params.PVALUE_THRESHOLD,

        )        

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation        

        create_directories([config.ROOT_DIR])

        data_transformation_config = DataTransformationConfig(
            root_dir= config.ROOT_DIR,    
            train_data_file= self.config.data_validation.VALID_TRAIN_FILE,
            test_data_file= self.config.data_validation.VALID_TEST_FILE, 
            train_npy_file = config.TRAIN_NPY_FILE,
            test_npy_file= config.TEST_NPY_FILE,
            target_column= self.params.TARGET_COLUMN,                       
            preprocessor_file= config.PREPROCESSOR_FILE

        )

        return data_transformation_config