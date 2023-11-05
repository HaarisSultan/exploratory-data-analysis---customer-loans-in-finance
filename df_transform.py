import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import yeojohnson as yeo    
    
class DataFrameTransform():
    def __init__(self):
        print("DataFrameTransform() loaded...")
        
    def replace_column_after_box_cox(self, df: pd.DataFrame, original_column: pd.Series, new_column: pd.Series):
        
        original_column_name = original_column.name
        
        # update original column's type to match the transformed data type
        df[original_column_name] = df[original_column_name].astype(str(new_column.dtype))

        # reassign the transformed data to the original column
        df[original_column_name] = new_column

        # replace any NA values introduced with the mean
        df[original_column_name].fillna(new_column.mean(), inplace=True)
        
        return df
    
    def box_cox_transform(self, column_data: pd.Series) -> pd.Series:
        return pd.Series(stats.boxcox(column_data)[0])
    
    def yeo_johnson_transform(self, column: pd.Series) -> pd.Series:
        return pd.Series(yeo(column)[0])
        
    def log_transform(self, column: pd.Series) -> pd.Series:
        if column.dtype == 'float64':
            new_column = column.map(lambda i: np.log(i) if i > 0.0 else 0.0)
        else:
            new_column = column.map(lambda i: np.log(i) if i > 0 else 0)
            
        return new_column
    
    def drop_column(self, df: pd.DataFrame, column_to_drop: pd.Series):
        return df.drop(column_to_drop.name, axis=1)
        
    def drop_columns(self, df: pd.DataFrame, columns_to_drop: pd.Series):
        column_names = list(columns_to_drop.index)
        return df.drop(column_names, axis=1)
        
    def drop_rows_of_null_column_entries(self, df: pd.DataFrame, column: pd.Series) -> pd.DataFrame:
        if str(column.dtype) == 'Int64':
            return df[~df[column.name].isna()]
        else:    
            to_drop = df[column.isnull()].index
            return df.drop(to_drop, axis=0) 
        
    def impute_nulls_in_column(self, column: pd.Series, strategy: str) -> pd.Series:
        
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

        

                    
