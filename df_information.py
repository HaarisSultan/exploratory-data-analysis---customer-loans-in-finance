import pandas as pd    
import numpy as np
from typing import List

def get_column(dataframe: pd.DataFrame, column_name: str) -> pd.Series:
    """Returns the column with name equal to the column_name parameter, from the given dataframe, provided the column exists.
    
        If such a column does not exist, an Exception is raised. The result is a pandas Series object.
    
        Args: 
            dataframe (pd.DataFrame): the dataframe from which to extract the column.
            column_name (str): the name of the column to extract 
    """
    
    if column_name not in dataframe.columns:
        # Alert the user that there is no such column
        raise Exception("Error: The column named {column_name} is not in the provided DataFrame.")
    else:
        # Enforce the Series type so python knows which methods are availble to the resultant column 
        column = pd.Series(dataframe[column_name])
        return column
    

class DataFrameInfo():
    """DataFrameInfo class contains methods that generate useful information about the DataFrame.
    
    Some useful utility methods you might want to create that are often used for EDA tasks are:
        
        - Describe all columns in the DataFrame to check their data types
        - Extract statistical values: median, standard deviation and mean from the columns and the DataFrame
        - Count distinct values in categorical columns
        - Print out the shape of the DataFrame
        - Generate a count/percentage count of NULL values in each column
        - Any other methods you may find useful
    """
    
    
    def __init__(self, df: pd.DataFrame):
        # Give the methods access to the dataframe to avoid extensive use of parameters 
        self.df = df  
        
    def column_contains_zero(self, column: pd.Series) -> bool:
        unique_values = list(column.unique())
        if column.dtype == 'float64':    
            if 0.0 in unique_values:
                return True
        elif column.dtype in ['int64', 'Int64']:
            if 0 in unique_values:
                return True
        return False
          
        
    def print_skew_and_dtype(self, dataframe: pd.DataFrame):
        skew_series = dataframe.skew(numeric_only=True).sort_values(ascending=False)
        columns = dataframe[list(skew_series.index)]
        column_types = columns.dtypes
        
        data = {
            "skewness": skew_series,
            "dtype": column_types
        }
        
        combo = pd.concat(data, axis=1)      
        return combo

    
    def measure_skew_for_all_columns(self, dataframe: pd.DataFrame, sort=False) -> pd.Series:

        skewness = dataframe.skew(numeric_only=True)
        
        if sort:
            skewness = dataframe.skew(numeric_only=True).sort_values(ascending=False)
        
        return skewness
    
    def print_null_removal_progress(self, dataframe: pd.DataFrame):
        # Extract only those columns with null values
        columns_with_nulls = self.get_columns_with_nulls(dataframe)

        # This displays both the # and % of nulls in the columns with nulls, good for debugging and tracking progress 
        null_info = self.combine_null_percentage_and_count(columns_with_nulls)
        
        message = f"I have {len(null_info)} columns to deal with:\n"
        return message, null_info
        
    def combine_null_percentage_and_count(self, columns: pd.DataFrame):

        # Create two series objects containing the count and percentage of nulls in those columns 
        percent_of_nulls = self.percentage_of_nulls_in_data_frame(dataframe=columns).sort_values(ascending=False)
        number_of_nulls = self.count_nulls_in_data_frame(dataframe=columns)
        column_types = columns.dtypes
        
        # Combine that data to display a DataFrame 
        data = {
            "% of nulls": percent_of_nulls,
            "# of nulls": number_of_nulls,
            "dtype": column_types
        }
        combo = pd.concat(data, axis=1)      
        return combo

    def contains_nulls(self, column: pd.Series) -> bool:
        return column.isnull().sum() != 0
        
    def get_columns_with_nulls(self, dataframe: pd.DataFrame):
        """Returns a DataFrame containing only columns which have null values."""
        
        # only_nulls = self.df[(self.df.isnull() == True)]
        only_nulls = dataframe.loc[:, dataframe.isna().any()]
        return only_nulls
    
    def describe_all(self):
        """Returns the count, mean, std, 25%/50%/75% quartiles, and maximum for every column, as a DataFrame."""
        
        description = self.df.describe()
        return description
    
    def show_all_column_dtypes(self):
        """Returns a Series of data types indexed with the column names."""
        
        return self.df.dtypes

    def describe_column(self, column: pd.Series):
        """For numerical columns, this returns the count, mean, std, 25%/50%/75% quartiles, and maximum for the given column, as a Series.
        
        For other types, it will return the count, number of unique values, the mode (top), and the frequency of the most common value.
        """
        
        return column.describe()
    
    def get_column_median(self, column: pd.Series):
        """Returns the median value of the column whose name matches the column_name parameter."""
        return column.median()
    
    def get_column_mean(self, column: pd.Series, precision=2) -> float:
        """Returns the mean value of the column whose name matches the column_name parameter.
                
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """
        mean = round(column.mean(), precision)
        return mean
    
    def get_column_mode(self, column: pd.Series) -> pd.Series:
        """Returns the mode of the column whose name matches the column_name parameter."""
        
        return column.mode()
    
    def get_column_standard_deviation(self, column: pd.Series, precision=2) -> float:
        """Returns the standard deviation of the column whose name matches the column_name parameter.
                
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.    
        """
        
        std = round(column.std(), precision)
        return std
    
    def get_distinct_categories_in_colum(self, column: pd.Series) -> List:
        """Returns a list of unique values in the given column, if that column is of type 'category'."""

        
        # This gets the names of the columns which are of type 'category' to ensure the provided column_name column is not of a different type
        category_columns = self.get_categorical_columns().columns
        
        if column.name not in list(category_columns):
            raise Exception(f"The column {column.name} is not of type category.")
        else:
            unique_values = list(column.unique())
            return unique_values
        
    
    def get_categorical_columns(self) -> pd.DataFrame:
        """Extracts only the columns of the DataFrame whose type is 'category'."""
        
        categorical_cols = self.df.select_dtypes("category")
        return categorical_cols
    
    def print_dataframe_shape(self) -> tuple[int, int]:
        """Returns the shape of the DataFrame."""
        
        return self.df.shape
    
    def count_nulls_in_data_frame(self, dataframe=None) -> pd.Series:
        """Returns a series showing the null count for every column in the dataframe."""
        
        if dataframe is None:
            # Apply to the entire dataframe
            null_series = self.df.isnull().sum()
            return null_series
        else:
            dataframe = pd.DataFrame(dataframe)
            # Apply to the provided dataframe 
            null_series = dataframe.isnull().sum()
            return null_series
    
    def percentage_of_nulls_in_data_frame(self, dataframe=None, precision=2) -> pd.Series:
        """Returns a series showing the percentage of null values for every column in the dataframe.
        
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
                dataframe: optinal argument to find the null percentage on a provided dataframe, e.g. a subset of the dataframe you know has nulls in.
        """        
        if dataframe is None:
            # Apply to the entire dataframe
            null_percentages = round(self.df.isnull().sum() * 100 / len(self.df), precision)
            return null_percentages
        else:
            dataframe = pd.DataFrame(dataframe)
            # Apply to the provided dataframe 
            null_percentages = round(dataframe.isnull().sum() * 100 / len(dataframe), precision)
            return null_percentages
        

    def count_nulls_in_column(self, column: pd.Series) -> int:
        """Return the total number of null values in the series."""
        
        null_count = column.isnull().sum()
        return null_count
    
    def percentage_of_nulls_in_column(self, column: pd.Series, precision=2) -> float:
        """Return the proportion of null values in the series as a percentage.
        
            Args:
                column_name (str): the name of the column to be accessed 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """
    
        null_percentage = round(column.isnull().sum() * 100 / len(column), precision)
        return null_percentage