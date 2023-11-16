import math
import numpy as np
import pandas as pd 

from pandas import DataFrame, Series
from typing import List


class DataTransform():
    """A class to transform columns in the DataFrame. 
    
    Attributes:
        None
    
    Methods:
        int64_to_category_with_ranges:
            Convert the Series given into a category type, and assign it's values to ranges.
        convert_float64_columns_into_Int64s:
            Convert the specified float64 columns in a DataFrame into int64.
        convert_object_columns_into_categories:
            Convert specified object columns in a DataFrame into category dtype.
        convert_obj_columns_to_date:
            Convert specified object columns in a DataFrame into datetime dtype.
        float64_to_int64:
            Convert float column to integer.
        object_to_int:
            Convert object column to integer using mapping.
        category_to_int:
            Convert category column to integer using mapping.
        object_to_categorical:
            Convert object column to category dtype.
        float_to_money_format:
            Convert a float to a string with commas to denote money.

    """
    def __init__(self):
        print("Loaded DataTransform()...")  
        
    def int64_to_category_with_ranges(self, df: DataFrame, column: Series) -> Series:
        """Convert the Series given into a category type, and assign it's values to ranges."""
        # Make copy to restore 0 values later
        orig_col = column.copy()  

        # Replace 0's with NaN
        rows_with_zero_index = df.loc[column == 0, column.name].index
        df.loc[column == 0, column.name] = np.nan

        # Calculate bin cutoffs for the non zero rows 
        non_zeros = df[~df.index.isin(rows_with_zero_index)][column.name]
        NUM_BINS = 4
        bin_size = (non_zeros.max() - non_zeros.min()) / NUM_BINS    
        bin_cutoffs = [int(non_zeros.max() - (bin_size * i)) for i in range(NUM_BINS, -1, -1)]
        
        # Determine the labels for each category 
        labels = [f"{math.floor(bin_cutoffs[i])}-{math.floor(bin_cutoffs[i+1])}" for i in range(NUM_BINS)]

        # Split the entries into their ranges - this also converts the column to categorical 
        column = pd.cut(column, bins=bin_cutoffs, labels=labels, include_lowest=True, right=False)

        # Add 0 category and restore the original 0 values from the copy 
        column = column.cat.add_categories("0")
        column.loc[orig_col == 0] = "0"

        return column
        
    def convert_float64_columns_into_Int64s(self, columns: DataFrame) -> DataFrame:
        """Convert the specified float64 columns in a DataFrame into int64."""
        return columns.astype("Int64")
    
    def convert_object_columns_into_categories(self, df: DataFrame, colnames: List[str]) -> DataFrame:
        """Convert specified object columns in a DataFrame into category dtype."""
        df[colnames] = df[colnames].astype("category")
        return df
    
    def convert_obj_columns_to_date(self, dataframe: DataFrame, column_names: List[str], current_format: str) -> DataFrame:
        """Convert specified object columns in a DataFrame into datetime dtype."""
        dataframe[column_names] = dataframe[column_names].apply(lambda x: pd.to_datetime(x, format=current_format))  
        return dataframe   

    def object_to_int(self, column: Series, mapping: dict) -> Series:
        """Convert object column to integer using mapping."""
        return Series(column.apply(lambda x: mapping[x])).astype('int64') 
    
    def float_to_money_format(self, value: float) -> str:
        """Convert a float to a string with commas to denote money."""
        return '£{:,.2f}'.format(value)        
    
    ########## ########## ##########
    # The following functions may have been used at some point in the project, but do not feature in the current EDA Notebook.    
    ########## ########## #########

    def category_to_int(self, column: Series, mapping: dict) -> Series:
        """Convert category column to integer using mapping."""
        return Series(column.apply(lambda x: mapping[x])).astype('int64')

    def float64_to_int64(self, column: Series) -> Series:
        """Convert float column to integer."""
        return column.fillna(0).astype(np.int64)
    
    def object_to_categorical(self, column: Series) -> Series:
        """Convert object column to category dtype."""
        return column.astype("category")