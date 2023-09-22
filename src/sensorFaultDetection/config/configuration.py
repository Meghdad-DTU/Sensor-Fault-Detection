from sensorFaultDetection.constants import *
from sensorFaultDetection.utils import read_yaml, create_directories
from sensorFaultDetection.entity.config_entity import DataIngestionConfig

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
            local_data_file= config.LOCAL_DATA_FILE
        )        

        return data_ingestion_config