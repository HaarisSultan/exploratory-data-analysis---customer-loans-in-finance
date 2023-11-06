import math
import numpy as np
import pandas as pd 
from typing import List
    
class DataTransform():
    def __init__(self):
        print("Loaded DataTransform()...")    
        
    def int_to_category_with_ranges(self, df, column):
        pass
    
    def float_to_category_with_ranges(self, df, column):
        pass
    
    def int64_to_category_with_ranges(self, dataframe: pd.DataFrame, column: pd.Series) -> pd.Series:
        
        # convert all values between 0-1 to NaN
        dataframe.loc[column == 0, column.name] = np.nan

        # work and the min and max values (where min is above 1)
        col_min = dataframe.loc[column > 0.0, str(column.name)].min() 
        col_max = dataframe.loc[column > 0, str(column.name)].max()

        num_bins = 4
        bin_size = (col_max - col_min) / num_bins
        bin_cutoffs = [col_min + (bin_size * i) for i in range(num_bins + 1)]

        labels = [f"{math.floor(bin_cutoffs[i])}-{math.floor(bin_cutoffs[i+1])}" for i in range(num_bins)]
        labels[0] = '1' + labels[0][1:]

        column = pd.cut(column, bin_cutoffs, labels=labels)

        column = column.cat.add_categories("0-1")

        column = column.fillna("0-1")
        
        return column
        
    def get_numeric_columns_from_df(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.select_dtypes(include=[np.number]) 
        
    def convert_float64_columns_into_int64s(self, columns: pd.DataFrame) -> pd.DataFrame:
        """Convert the specified float64 columns in a DataFrame into int64.

            Args:
                columns: A dataframe of float64 columns to convert to int64.

            Returns:
                The modified dataframe.                
        """
        
        return columns.astype("Int64")

    
    def convert_object_columns_into_categories(self, columns: pd.DataFrame) -> pd.DataFrame:
        """Convert specified object columns in a DataFrame into category dtype.

            Args:
                column_names: A list of column names to convert from object to category.

            Returns: 
                The modified dataframe.
            
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
        
        return columns.astype("category")
    
    def convert_obj_columns_to_date(self, dataframe: pd.DataFrame, column_list: pd.DataFrame, current_format: str) -> pd.DataFrame:
        """Convert specified object columns in a DataFrame into datetime dtype.

            Args:
                column_list: A dataframe containing the columns to alter.
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
        for column in column_list:
            dataframe[column]= pd.to_datetime(column_list[column], format=current_format)
        
        return dataframe      
    
    def object_to_date(self, column: pd.Series, current_format: str):
        """Convert object column to datetime."""
        return pd.to_datetime(column, format=current_format)

    def float64_to_int64(self, column: pd.Series) -> pd.Series:
        """Convert float column to integer."""
        return column.fillna(0).astype(np.int64)

    def object_to_int(self, column: pd.Series, mapping: dict) -> pd.Series:
        """Convert object column to integer using mapping.

        Args:
            column: Column to convert
            mapping: Mapping of values to integers
        """
        return column.apply(lambda x: mapping[x] if x is not np.nan else x)

    def object_to_categorical(self, column: pd.Series) -> pd.Series:
        """Convert object column to category dtype."""
        return column.astype("category")
        
        
