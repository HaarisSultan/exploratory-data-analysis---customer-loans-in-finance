import pandas as pd
from typing import List

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
        
    def impute_nulls_in_columns(self, columns_to_impute: List[pd.Series], replace_with):
        
        if replace_with not in ['mean', 'median']:
            raise Exception(f"The parameter 'replace_with' accepts either 'mean' or 'median'. You entered '{replace_with}'.")
        else:
            
            for column in columns_to_impute:
                if replace_with is 'mean':
                    column.fillna(column.mean(), inplace=True)
                else:
                    column.fillna(column.median(), inplace=True)
