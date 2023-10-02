import sys
from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.config.configuration import ConfigurationManager
from sensorFaultDetection.components.prediction import Prediction


STAGE_NAME = "Prediction Pipeline"

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        

    def predict(self):
        config = ConfigurationManager()
        prediction_config = config.get_prediction_config()
        prediction = Prediction(filename=self.filename, config=prediction_config)
        df = prediction.initiate_prediction()
        return df