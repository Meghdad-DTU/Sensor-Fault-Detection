import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from sensorFaultDetection.pipeline.stage_02_data_validation import DataValidationPipeline
from sensorFaultDetection.pipeline.stage_03_data_transformation import DataTransformationPipeline
from sensorFaultDetection.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from sensorFaultDetection.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline
#from sensorFaultDetection.pipeline.training_pipeline import TrainingPipeline
#from sensorFaultDetection.pipeline.prediction_pipeline import PredictionPipeline


STAGE_NAME = "Data Ingestion Stage"

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
    raise CustomException(e, sys)


STAGE_NAME = "Model Training Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = ModelTrainerPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)

STAGE_NAME = "Model Evaluation Stage"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = ModelEvaluationPipeline()
    obj.main()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)

'''STAGE_NAME = "Training Pipeline"

try:
    logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
    obj = TrainingPipeline()
    obj.run_pipeline()
    logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
    
except Exception as e:
    raise CustomException(e, sys)

file_path = 'artifacts/data_validation/valid/test.csv'
STAGE_NAME = "Prediction Pipeline"

if __name__ == "__main__":    
    try:        
        logging.info(f'>>>>>>> stage {STAGE_NAME} started <<<<<<<<')
        obj = PredictionPipeline(file_path)
        df = obj.predict()
        logging.info(f'>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
    
    except Exception as e:
        raise CustomException(e, sys)'''