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