import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.config.configuration import ConfigurationManager
from sensorFaultDetection.components.model_evaluation import ModelEvaluation


STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.initiate_model_evaluation()    


if __name__ == "__main__":    
    try:        
        logging.info(f'>>>>>>> stage {STAGE_NAME} started <<<<<<<<')
        obj = ModelEvaluationPipeline()
        obj.main()
        logging.info(f'>>>>>>> stage {STAGE_NAME} completed <<<<<<<<')
    
    except Exception as e:
        raise CustomException(e, sys)