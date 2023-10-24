import pandas as pd
import numpy as np
from typing import List

def check_no_nulls(column: pd.Series):
    # Verify that all nulls were removed 
    if column.isnull().sum() != 0:
        raise Exception(f"Error: impute_nulls_in_column() was not able to remove all null's from {column.name}. There are still {column.isnull().sum()} null values.")
    
    
def check_is_valid_strategy(strategy: str):
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
        self.df = dataframe
    
    def drop_columns_by_name(self, column_names: List[str]):
        self.df.drop(column_names, axis=1, inplace=True)
    
    def drop_null_rows_by_column_name(self, column_name: str):
        df = self.df
    
        to_drop = self.df[self.df[column_name].isnull()].index
        df = df.drop(to_drop, axis=0)
        
        return df
        
    def impute_nulls_in_column(self, column_name: str, strategy: str) -> pd.Series:
        
        # Raise an error if the imputation strategy is not recognised
        check_is_valid_strategy(strategy)
        
        column = get_column(self.df, column_name=column_name)
        
        if strategy is 'mean':
            column = column.fillna(column.mean()[0])
        elif strategy is 'median':
            if column.dtype in ['float64', 'int64']:
                column = column.fillna(column.median())
            else:
                column = column.fillna(column.median()[0])
        else:
            column = column.fillna(column.mode()[0])
            
        # Raise an error if the above failed to remove all nulls from the column
        check_no_nulls(column)

        return column

        

                    
