import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.config.configuration import ConfigurationManager
from sensorFaultDetection.components.data_ingestion import DataIngestion


STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.dowload_file()
        data_ingestion.train_test_creation()


if __name__ == "__main__":    
    try:        
        logging.info(f'>>>>>>> stage {STAGE_NAME} started <<<<<<<<')
        obj = DataIngestionPipeline()
        obj.main()
        logging.info(f'>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
    
    except Exception as e:
        raise CustomException(e, sys)
