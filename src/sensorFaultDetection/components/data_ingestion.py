import os
from pathlib import Path
import pandas as pd
from io import StringIO
import boto3
from sensorFaultDetection.utils import get_size
from sensorFaultDetection.logger import logging
from sensorFaultDetection.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.client = boto3.client('s3',
                      aws_access_key_id=self.config.s3_key,
                      aws_secret_access_key=self.config.s3_secret_key
                      )


    def dowload_file(self):
        if not os.path.exists(self.config.local_data_file):
            csv_obj = self.client.get_object(Bucket=self.config.s3_bucket, Key=self.config.object_key)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_string))
            df.to_csv(self.config.local_data_file, index=False, header=True)
            logging.info(f'{self.config.local_data_file} is downloaded!')            

        else:
            logging.info(f"File alraedy exists of size : {get_size(Path(self.config.local_data_file))}")