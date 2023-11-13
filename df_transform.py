import pandas as pd
import numpy as np

from pandas import DataFrame, Series
from scipy import stats
from scipy.stats import yeojohnson as yeo    
from typing import List
    
    
class DataFrameTransform():
    """A class containing methods to transform pandas DataFrames.

    Attributes:
        None
    
    Methods:
        replace_column_after_box_cox: Replaces a DataFrame column with a transformed version, handling dtype changes and NaN values.
        box_cox_transform: Applies a Box-Cox transform to a Series and returns the result.
        yeo_johnson_transform: Applies a Yeo-Johnson transform to a Series and returns the result. 
        log_transform: Applies a log transform to a Series and returns the result.
        drop_column: Drops a specified column from a DataFrame.
        drop_columns: Drops specified columns from a DataFrame.
        drop_rows_of_null_column_entries: Drop rows with NaN values in DataFrame columns specified by column_names.
        impute_nulls_in_column: Imputes NaN values in a Series using mean, median or mode.

    """
    
    def __init__(self):
        print("Loaded DataFrameTransform()...")
        
    def replace_column_after_box_cox(self, df: DataFrame, original_column: Series, new_column: Series) -> DataFrame:
        """Replace a DataFrame column with a transformed version."""
        original_column_name = original_column.name
        
        # update original column's type to match the transformed data type
        df[original_column_name] = df[original_column_name].astype(str(new_column.dtype))

        # reassign the transformed data to the original column
        df[original_column_name] = new_column

        # replace any NA values introduced with the mean
        df[original_column_name].fillna(new_column.mean(), inplace=True)
        
        return df
    
    def calculate_revenue(self, data: DataFrame) -> int:
        """Use revenue formula to get the sum of revenues for a Series of loans."""
        return pd.Series(data['loan_amount'] * (data['int_rate'] / 12) * data['term']).sum()
        
    def box_cox_transform(self, column_data: Series) -> Series:
        """Apply a Box-Cox transform to a Series."""
        return Series(stats.boxcox(column_data)[0])
    
    def yeo_johnson_transform(self, column: Series) -> Series:
        """Apply a Yeo-Johnson transform to a Series."""
        return Series(yeo(column)[0])
        
    def log_transform(self, column: Series) -> Series:
        """Apply a log transform to a Series."""
        if column.dtype == 'float64':
            new_column = column.map(lambda i: np.log(i) if i > 0.0 else 0.0)
        else:
            new_column = column.map(lambda i: np.log(i) if i > 0 else 0)      
        return new_column
    
    def drop_column(self, df: DataFrame, column_to_drop: Series) -> DataFrame:
        """Drop a specified column from a DataFrame."""
        return df.drop(column_to_drop.name, axis=1)
        
    def drop_columns(self, df: DataFrame, column_names: List[str]) -> DataFrame:
        """Drop specified columns from a DataFrame."""
        return df.drop(column_names, axis=1)
    
    def drop_rows_of_null_column_entries(self, df: DataFrame, column_names: List[str]) -> DataFrame:
        """Drop rows with NaN values in DataFrame columns specified by column_names."""
        
        for column_name in column_names:
            column = df[column_name]
            
            if str(column.dtype) == 'Int64':
                df = df[~df[column.name].isna()]
            else:    
                to_drop = df[column.isnull()].index
                df = df.drop(to_drop, axis=0) 
                
        return df
        
    def impute_nulls_in_column(self, column: Series, strategy: str) -> Series:
        """Impute NaN values in a Series using mean, median or mode."""
        
        # Raise an error if the imputation strategy is not recognised
        if strategy not in ['mean', 'median', 'mode']:
            raise Exception(f"The parameter 'replace_with' accepts either 'mean', 'median' or 'mode'. You entered '{strategy}'.")  
              
        if strategy == 'mean':
            column = column.fillna(column.mean()[0])
        elif strategy == 'median':
            if column.dtype in ['float64', 'int64']:
                column = column.fillna(column.median())
            else:
                column = column.fillna(column.median()[0])
        else:
            column = column.fillna(column.mode()[0])
            
        # Raise an error if the above failed to remove all nulls from the column
        if column.isnull().sum() != 0:
            raise Exception(f"Error: impute_nulls_in_column() was not able to remove all null's from {column.name}. There are still {column.isnull().sum()} null values.")
        
        return column