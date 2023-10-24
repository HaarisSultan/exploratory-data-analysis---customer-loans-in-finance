import numpy as np
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
    
class DataTransform():
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
    
    def get_numeric_columns_from_df(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.select_dtypes(include=[np.number]) 
        
    def convert_float64_columns_into_int64s(self, column_names: List[str]):
        """Convert the specified float64 columns in a DataFrame into int64.

            Args:
                column_names: A list of string column names to convert from float64 to int64.

            Returns:
                None. The dataframe is modified in-place.

            Raises:
                ValueError: If any of the specified columns do not exist in the DataFrame.

            This converts the data type for the specified columns from float64 to int64. 
            Any NaN values in the columns are replaced with 0 before converting.

            Example:
                
                df = pd.DataFrame({'A': [1.2, 3.4], 'B': [5.6, 7.8]}) 
                cols = ['A', 'B']
                convert_float64_columns_into_int64s(cols)
                
                print(df.dtypes)
                
                A      int64
                B      int64
                dtype: object
        """
        
        for column_name in column_names:
            column = get_column(self.df, column_name=column_name)

            self.df[column_name] = column.astype("Int64")
            # self.df[column_name] = column.fillna(0).astype(np.int64)
    
    
    def convert_object_columns_into_categories(self, column_names: List[str]):
        """Convert specified object columns in a DataFrame into category dtype.

            Args:
                column_names: A list of column names to convert from object to category.

            Returns: 
                None. The DataFrame is modified in-place.
            
            Raises:
                KeyError: If any column in column_names does not exist in the DataFrame.
                
            Converts the specified object columns into Pandas category dtype to reduce
            memory usage.
                
            Example:
                
                df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': ['x', 'y', 'z']})
                cols = ['A'] 
                convert_object_columns_into_categories(cols)
                
                print(df.dtypes)
                
                A    category
                B    object
                dtype: object
        """
        for column_name in column_names:
            column = get_column(self.df, column_name=column_name)
            self.df[column_name] = column.astype("category")
                
    
    def convert_object_columns_to_date(self, column_names: List[str], current_format: str):
        """Convert specified object columns in a DataFrame into datetime dtype.

            Args:
                column_names: A list of column names to convert from object to datetime.
                current_format: The strftime format string specifying how the date is currently
                                formatted in the object columns.
                                
            Returns:
                None. The DataFrame is modified in-place.
                
            Raises:
                KeyError: If any column in column_names does not exist in the DataFrame.
                ValueError: If any date values fail to parse with the supplied format.
                
            Converts the specified object columns containing date strings into Pandas 
            datetime dtype using pd.to_datetime().
                
            Example:
                
                df = pd.DataFrame({'Date': ['01/01/2020', '02/01/2020']})
                cols = ['Date']
                fmt = '%m/%d/%Y'
                convert_object_columns_to_date(cols, fmt)
                
                print(df)
                
                # Output:
                Date
                0 2020-01-01
                1 2020-02-01
        """
        for column_name in column_names:
            column = get_column(self.df, column_name=column_name)
            self.df[column_name]= pd.to_datetime(column, format=current_format)        
    
    def object_to_date(self, column_name: str, current_format: str):
        """Convert object column to datetime.

        Args:
            column_name: Name of column to convert
            current_format: Format string for existing dates
        """
        
        column = get_column(self.df, column_name)
        new_col = pd.to_datetime(column, format=current_format)
        return new_col

    def float64_to_int64(self, column_name: str) -> pd.Series:
        """Convert float column to integer.
        
        Args:
            column_name: Name of column to convert
        """
        
        column = get_column(self.df, column_name)
        column = column.fillna(0).astype(np.int64)
        return column

    def object_to_int(self, column_name: str, mapping: dict) -> pd.Series:
        """Convert object column to integer using mapping.

        Args:
            column_name: Name of column to convert
            mapping: Mapping of values to integers
        """
        
        column = get_column(self.df, column_name)
        updated_column = column.apply(lambda x: mapping[x] if x is not np.nan else x)
        return updated_column

    def object_to_categorical(self, column_name: str) -> pd.Series:
        """Convert object column to category dtype.
        
        Args: 
            column_name: Name of column to convert
        """
        
        column = get_column(self.df, column_name)
        column = column.astype("category")
        return column
        
        
