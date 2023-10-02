from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    s3_bucket: str
    s3_key: str
    s3_secret_key: str
    object_key: Path
    local_data_file: Path
    train_test_ratio: float
    train_data_file: Path
    test_data_file: Path
    drop_columns: list

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    train_data_file: Path
    test_data_file: Path    
    valid_train_file: Path
    valid_test_file: Path
    invalid_train_file: Path
    invalid_test_file: Path    
    drift_report_file: Path
    schema_columns: list
    schema_numerical_columns: list    
    pvalue_threshold: float

@dataclass(frozen= True)
class DataTransformationConfig:
    root_dir: Path  
    train_data_file: Path
    test_data_file: Path  
    train_npy_file : Path
    test_npy_file: Path 
    target_column: str 
    preprocessor_file: Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_npy_file: Path
    test_npy_file: Path
    expected_accuracy_threshold: float
    overfit_underfit_threshold: float
    preprocessor_file: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path    
    trained_model_path: Path    
    valid_train_file: Path
    valid_test_file: Path
    evaluation_report_file: Path
    model_evaluation_changed_threshold: float
    target_column: str

@dataclass(frozen=True)
class PredictionConfig:   
    best_model_dir: Path
    input_variables: list
    target_column: str