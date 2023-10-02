import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from sensorFaultDetection.pipeline.stage_02_data_validation import DataValidationPipeline
from sensorFaultDetection.pipeline.stage_03_data_transformation import DataTransformationPipeline
from sensorFaultDetection.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from sensorFaultDetection.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline



class TrainingPipeline:
    is_pipeline_running= False
    def __init__(self):
        pass

    def run_pipeline(self):
        try: 
            TrainingPipeline.is_pipeline_running = True       
            STAGE_NAME = "Data Ingestion Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            obj = DataIngestionPipeline()
            obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<') 

            STAGE_NAME = "Data Validation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            obj = DataValidationPipeline()
            obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')

            STAGE_NAME = "Data Transformation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            obj = DataTransformationPipeline()
            obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')

            STAGE_NAME = "Model Training Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            obj = ModelTrainerPipeline()
            obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')                


            STAGE_NAME = "Model Evaluation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            obj = ModelEvaluationPipeline()
            obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
            
            TrainingPipeline.is_pipeline_running = True    
        
        except Exception as e:
            raise CustomException(e, sys)  
        

