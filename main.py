import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.pipeline.stage_01_data_ingestion import DataIngestionPipeline


STAGE_NAME = "Data Ingestion Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = DataIngestionPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)