import os
import sys
import yaml
import pickle

from sensorFaultDetection.logger import logging
from sensorFaultDetection.exception import CustomException


from typing import Any
from box import ConfigBox
from ensure import ensure_annotations
from pathlib import Path



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    reads yaml file and returns
    Args:
        path to yaml (str): path like input
    Raises:
        valueError
    Returns:
        configBox: configBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f'yaml file {yaml_file.name} loaded successfully')
            return ConfigBox(content)
            
    except Exception as e:
        raise CustomException(e, sys)   


def write_yaml_file(path_to_yaml: Path, content: object, replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(path_to_yaml):
                os.remove(path_to_yaml)
        os.makedirs(os.path.dirname(path_to_yaml), exist_ok=True)
        with open(path_to_yaml, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
        logging.info(f'yaml file {yaml_file.name} saved successfully')

    except Exception as e:
        raise CustomException(e, sys)        




@ensure_annotations
def create_directories(path_to_directories: list, verbos=True):
    """
    create list of directories
    Args:
    path_to_directories(list): list of path of directories
    ignore_log(bool, optional): ignore if multiple dirs is to be created. Defaults to be False
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbos:
            logging.info(f'created directory at {path}')

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

#@ensure_annotations
def save_pickle(path: Path, obj:Any):
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