import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from sensorFaultDetection.pipeline.stage_02_data_validation import DataValidationPipeline
from sensorFaultDetection.pipeline.stage_03_data_transformation import DataTransformationPipeline
from sensorFaultDetection.pipeline.stage_04_model_trainer import ModelTrainerPipeline

'''STAGE_NAME = "Data Ingestion Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = DataIngestionPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)


STAGE_NAME = "Data Validation Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = DataValidationPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)


STAGE_NAME = "Data Transformation Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = DataTransformationPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)'''


STAGE_NAME = "Model Training Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = ModelTrainerPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)