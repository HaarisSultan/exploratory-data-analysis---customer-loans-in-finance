import pandas as pd
import numpy as np
from scipy import stats
from typing import List
from plotter import Plotter
from scipy.stats.mstats import winsorize
from scipy.stats import yeojohnson as yeo

def check_no_nulls(column: pd.Series):
    # Verify that all nulls were removed 
    if column.isnull().sum() != 0:
        raise Exception(f"Error: impute_nulls_in_column() was not able to remove all null's from {column.name}. There are still {column.isnull().sum()} null values.")
    
    
def check_is_valid_strategy(strategy: str):
    """Check that the imputation strategy chosen is one of mean, median or mode."""
    
    if strategy not in ['mean', 'median', 'mode']:
        raise Exception(f"The parameter 'replace_with' accepts either 'mean', 'median' or 'mode'. You entered '{strategy}'.")
    
def get_column(dataframe: pd.DataFrame, column_name: str) -> pd.Series:
    """Return a column Series from a DataFrame.

        Args:
            dataframe: Pandas DataFrame to extract column from.
            column_name: Name of column to extract.

        Returns:
            Pandas Series containing the extracted column.

        Raises:
            Exception: If column_name does not exist in the DataFrame.

        Example:
            
            df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
            
            col = get_column(df, 'A')
            
            print(col)
            
            0    1
            1    2
            Name: A, dtype: int64
    """
    
    if column_name not in dataframe.columns:
        # Alert the user that there is no such column
        raise Exception("Error: The column named {column_name} is not in the provided DataFrame.")
    else:
        # Enforce the Series type so python knows which methods are availble to the resultant column 
        column = pd.Series(dataframe[column_name])
        return column
    
class DataFrameTransform():
    def __init__(self, dataframe: pd.DataFrame):
        print("DataFrameTransform loaded...")
        
    def replace_column_after_box_cox(self, df: pd.DataFrame, original_column: pd.Series, new_column: pd.Series):
        
        og_col_name = original_column.name
        
        # update original column type to match the transformed data 
        df[og_col_name] = df[og_col_name].astype(str(new_column.dtype))

        # reassign the transformed data to the original column
        df[og_col_name] = new_column

        # replace any NA values introduced with the mean
        df[og_col_name].fillna(new_column.mean(), inplace=True)
        
        return df
    
    def box_cox_transform(self, column_data: pd.Series) -> pd.Series:
        column_data = pd.Series(stats.boxcox(column_data)[0])
        return column_data
    
    def yeo_johnson_transform(self, column: pd.Series) -> pd.Series:
        return pd.Series(yeo(column)[0])
        
    def log_transform(self, column: pd.Series) -> pd.Series:
        if column.dtype == 'float64':
            new_column = column.map(lambda i: np.log(i) if i > 0.0 else 0.0)
        else:
            new_column = column.map(lambda i: np.log(i) if i > 0 else 0)
        return new_column
    
    def drop_column(self, df: pd.DataFrame, column_to_drop: pd.Series):
        df = df.drop(column_to_drop.name, axis=1)
        return df
    
    def drop_columns(self, df: pd.DataFrame, columns_to_drop: pd.Series):
        column_names = list(columns_to_drop.index)
        df = df.drop(column_names, axis=1)
        return df
    
    def drop_rows_of_null_column_entries(self, df: pd.DataFrame, column: pd.Series) -> pd.DataFrame:
        if str(column.dtype) == 'Int64':
            df = df[~df[column.name].isna()]
            return df 
        else:    
            to_drop = df[column.isnull()].index
            df = df.drop(to_drop, axis=0) 
            return df
        
    def impute_nulls_in_column(self, column: pd.Series, strategy: str) -> pd.Series:
        
        # Raise an error if the imputation strategy is not recognised
        check_is_valid_strategy(strategy)
        
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
        check_no_nulls(column)
    
        return column

        

                    
