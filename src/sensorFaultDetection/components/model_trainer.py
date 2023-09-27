import sys
import pandas as pd
from sensorFaultDetection. logger import logging
from sensorFaultDetection.exception import CustomException
from sensorFaultDetection.utils import load_numpy_array, confusion_matrix_display, classifier_performance_report, save_pickle, load_pickle
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sensorFaultDetection.entity.config_entity import ModelTrainerConfig


class SensorModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        try:
            self.preprocessing_object = preprocessing_object
            self.trained_model_object = trained_model_object
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        logging.info("Entered predict method of SensorTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise CustomException(e, sys) 

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def perform_hyper_parameter_tuning(self):
        pass
    
    def train_model(self, X_train, y_train):
        try:
            xgb_classifier = XGBClassifier()
            xgb_classifier.fit(X_train, y_train)
            return xgb_classifier

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self):
        try:
            # loading train and test arr
            train_arr = load_numpy_array(self.config.train_npy_file)
            test_arr = load_numpy_array(self.config.test_npy_file) 

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )           
            
            model = self.train_model(X_train, y_train)
            logging.info("Training model is completed successfully!")
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            labels = ["Negative", "Positive"]

            confusion_matrix_display(
                y_true = y_train, 
                y_pred = y_train_pred, 
                path= self.config.train_confusion_matrix_file, 
                classes=labels
                )
            train_metric_table= classifier_performance_report(
                y_true= y_train,
                y_pred= y_train_pred, 
                path= self.config.train_model_performance_file, 
                classes=labels
                )
            logging.info(f"Model performance metrics for train data is completed and stored at {self.config.train_model_performance_file}!")
            
            confusion_matrix_display(
                y_true = y_test, 
                y_pred = y_test_pred, 
                path= self.config.test_confusion_matrix_file, 
                classes=labels
                )
            test_metric_table = classifier_performance_report(
                y_true= y_test, 
                y_pred= y_test_pred, 
                path= self.config.test_model_performance_file, 
                classes=labels
                )
            logging.info(f"Model performance metrics for test data is completed and stored at {self.config.test_model_performance_file}!")

            if train_metric_table['f1-score'].values[-1] < self.config.expected_accuracy_threshold:
                raise Exception("Trained model is not good to provide expected accuracy!")

            # Overfitting and Underfitting:
            # Check whether there is a significant difference between f1-score for both train and test or not            

            diff = abs(train_metric_table['f1-score'].values[-1] - test_metric_table['f1-score'].values[-1])            
            if diff > self.config.overfit_underfit_threshold:
                raise Exception("Model is not good, try to do more investigation")
            
            preprocessor = load_pickle(self.config.preprocessor_file)
            sensor_model = SensorModel(preprocessing_object= preprocessor, trained_model_object= model)            

            save_pickle(path= self.config.trained_model_path, obj= sensor_model)

        except Exception as e:
            raise CustomException(e, sys)