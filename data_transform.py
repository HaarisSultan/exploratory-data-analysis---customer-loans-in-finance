import numpy as np
import pandas as pd 

class DataTransform():
    def __init__(self):
        print("Loaded DataTransform class.")
        
    @staticmethod
    def object_to_date(column: pd.Series, current_format):
        new_col = pd.to_datetime(column, format=current_format)
        return new_col
    
    def float64_to_int64(column: pd.Series):
        column = column.fillna(0).astype(np.int64)
        return column
    
    @staticmethod
    def object_to_int(column: pd.Series, mapping: dict):
        updated_column = column.apply(lambda x: mapping[x] if x is not np.nan else x)
        return updated_column
        
    @staticmethod
    def object_to_categorical(column: pd.Series):
        column = column.astype("category")
        return column
        
        
