import sys
from datetime import datetime
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from sensorFaultDetection.pipeline.stage_02_data_validation import DataValidationPipeline
from sensorFaultDetection.pipeline.stage_03_data_transformation import DataTransformationPipeline
from sensorFaultDetection.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from sensorFaultDetection.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline
from sensorFaultDetection.config.configuration import ConfigurationManager
from sensorFaultDetection.entity.config_entity import TrainingPipelineConfig
from sensorFaultDetection.cloud_storage.s3_syncer import S3Sync



class TrainingPipeline:
    is_pipeline_running= False
    def __init__(self, config: TrainingPipelineConfig):
        self.config = config        

    def sync_artifact_dir_to_s3(self):
        try:
            now = datetime.now
            timestamp = format(now().strftime('%Y-%m-%d_%H:%M:%S'))
            aws_bucket_url = f's3://{self.config.training_bucket_name}/artifacts/{timestamp}'
            S3Sync.sync_folder_to_s3(folder= self.config.artifacts_dir, aws_bucket_url= aws_bucket_url)
        except Exception as e:
            raise CustomException(e, sys)
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f's3://{self.config.training_bucket_name}/{self.config.saved_model_dir}'
            S3Sync.sync_folder_to_s3(folder= self.config.saved_model_dir, aws_bucket_url= aws_bucket_url)
        except Exception as e:
            raise CustomException(e, sys)
    
    def run_pipeline(self):
        try: 
            TrainingPipeline.is_pipeline_running = True       
            STAGE_NAME = "Data Ingestion Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            dataIngestion_obj = DataIngestionPipeline()
            dataIngestion_obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<') 

            STAGE_NAME = "Data Validation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            dataValidation_obj = DataValidationPipeline()
            dataValidation_obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')

            STAGE_NAME = "Data Transformation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            dataTransformation_obj = DataTransformationPipeline()
            dataTransformation_obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')

            STAGE_NAME = "Model Training Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            modelTrainer_obj = ModelTrainerPipeline()
            modelTrainer_obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')

            STAGE_NAME = "Model Evaluation Stage"

            logging.info(f'>>>>>>> {STAGE_NAME} started <<<<<<<<')
            modelEvaluation_obj = ModelEvaluationPipeline()
            modelEvaluation_obj.main()
            logging.info(f'>>>>>>> {STAGE_NAME} completed <<<<<<<<')
            
            if not modelEvaluation_obj.is_model_accepted:
                self.sync_artifact_dir_to_s3()
                logging.info('The artifacts are uploaded in aws s3!')
            else:
                self.sync_artifact_dir_to_s3()
                self.sync_saved_model_dir_to_s3()
                logging.info('The artifacts and model are uploaded in aws s3!')           
            
            
            TrainingPipeline.is_pipeline_running = False           
        
        except Exception as e:
            TrainingPipeline.is_pipeline_running = False 
            raise CustomException(e, sys)  
        

STAGE_NAME = 'Training Pipeline'
if __name__ == "__main__":    
    try:        
        logging.info(f'>>>>>>> stage {STAGE_NAME} started <<<<<<<<')
        config = ConfigurationManager()
        training_pipeline_config = config.get_training_pipeline_config()
        training_pipeline = TrainingPipeline(config=training_pipeline_config)
        training_pipeline.run_pipeline()    
        logging.info(f'>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
    
    except Exception as e:
        raise CustomException(e, sys)