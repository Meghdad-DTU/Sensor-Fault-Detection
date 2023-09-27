import os
import sys
import yaml
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_recall_fscore_support

from typing import Any
from box import ConfigBox
from ensure import ensure_annotations
from pathlib import Path



@ensure_annotations
def read_yaml(path: Path) -> ConfigBox:
    """
    reads yaml file and returns
    Args:
        path (str): path to input
    Raises:
        valueError
    Returns:
        configBox: configBox type
    """
    try:
        with open(path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f'yaml file {yaml_file.name} loaded successfully')
            return ConfigBox(content)
            
    except Exception as e:
        raise CustomException(e, sys)   


def write_yaml_file(path: Path, content: object, replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(path):
                os.remove(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
        logging.info(f'yaml file {yaml_file.name} saved successfully')

    except Exception as e:
        raise CustomException(e, sys)        

def save_numpy_array(path: Path, array: np.array):
    """
    save numpy array to file
    Args:
        path (str): path to save the file
        array (np.array): data to save
    """
    try:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'wb') as file_obj:
            np.save(file_obj, array)
            logging.info(f'created .npy file at {path}')

    except Exception as e:
        raise CustomException(e, sys)

    
def load_numpy_array(path: Path):
    """
    load numpy array from file
    Args:
        path (str): path to load the file        
    """
    try:        
        with open(path, 'rb') as file_obj:
            npy_file = np.load(file_obj)
            logging.info(f'.npy file is loaded successfully from {path}!')
        return  npy_file       

    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def create_directories(path_to_directories: list, verbos=True):
    """
    create list of directories
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to be False
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbos:
                logging.info(f'created directory at {path}')
    except Exception as e:
        raise CustomException(e, sys)

@ensure_annotations
def get_size(path: Path) -> str:
    """
    get size in KB
    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    try:
        size_in_kb = round(os.path.getsize(path)/1024)
        return f"~ {size_in_kb} KB"
    except Exception as e:
        raise CustomException(e, sys)

#@ensure_annotations
def save_pickle(path: Path, obj: object) -> None:
    """
    save object as pickel 
    Args:
        path (Path): path to .pkl 
        obj : object to be saved in the file             
    """
    try:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"pickel file saved at {path}")
    
    except Exception as e:
            raise CustomException(e, sys)
    

#@ensure_annotations
def load_pickle(path: Path) -> object:
    """
    Load object as pickel 
    Args:
        path (Path): path to .pkl                     
    """
    try:
        if not os.path.exists(path): 
            raise Exception(f'The file: {path} does not exist!')      
        
        with open(path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
            logging.info(f"pickel file is loaded successfully from {path}!")
            return obj            
    
    except Exception as e:
            raise CustomException(e, sys)
    

def confusion_matrix_display(y_true: np.array, y_pred: np.array, path: Path, classes: list=None) -> None:
    """
    This function saves confusion matrix
    Args:
        y_true (np.array): actual value of y
        y_pred (np.array): predicted valuye of y
        path (Path): path to save confusion matrix
        classes (list): label classes to be predicted
        
    """
    try:
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
        disp.plot(cmap=plt.cm.Blues)
        plt.savefig(path)             
        plt.close()
    except Exception as e:
        raise CustomException

def classifier_performance_report(y_true: np.array, y_pred: np.array,  path: Path, classes: list=None) -> pd.DataFrame:
    """
    This function returns scikit learn output metrics.classification_report 
    into CSV/tab-delimited format
    Args:
        y_true (np.array): the actual value of y
        y_pred (np.array): the predicted valuye of y
        path (Path): path to save model performance metrics
        classes (np.array): list of label classes to be predicted

    """
    try:
        metrics_summary = precision_recall_fscore_support(y_true=y_true, y_pred=y_pred)    
        avg = list(precision_recall_fscore_support(y_true=y_true, y_pred=y_pred, average='weighted'))
        metrics_sum_index = ['precision', 'recall', 'f1-score', 'support']
        class_report_df = pd.DataFrame(list(metrics_summary), index=metrics_sum_index)

        support = class_report_df.loc['support']
        total = support.sum() 
        avg[-1] = total

        class_report_df['avg / total'] = avg              
        metrics_table = class_report_df.T
        metrics_table.index = classes + ['avg / total']
        metrics_table.to_csv(path, index=True, header=True) 
        return metrics_table  
        
    except Exception as e:
        raise CustomException(e, sys)