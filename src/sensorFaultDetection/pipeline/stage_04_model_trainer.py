import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.config.configuration import ConfigurationManager
from sensorFaultDetection.components.model_trainer import ModelTrainer


STAGE_NAME = "Model Training Stage"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.initiate_model_trainer()    


if __name__ == "__main__":    
    try:        
        logging.info(f'>>>>>>> stage {STAGE_NAME} started <<<<<<<<')
        obj = ModelTrainerPipeline()
        obj.main()
        logging.info(f'>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
    
    except Exception as e:
        raise CustomException(e, sys)