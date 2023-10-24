import pandas as pd    
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
    def __init__(self, df: pd.DataFrame):
        # Give the methods access to the dataframe to avoid extensive use of parameters 
        self.df = df
        
    def describe_all(self):
        """Returns the count, mean, std, 25%/50%/75% quartiles, and maximum for every column, as a DataFrame."""
        
        description = self.df.describe()
        return description
    
    def show_all_column_dtypes(self):
        """Returns a Series of data types indexed with the column names."""
        
        return self.df.dtypes

    def describe_column(self, column_name: str):
        """For numerical columns, this returns the count, mean, std, 25%/50%/75% quartiles, and maximum for the given column, as a Series.
        
        For other types, it will return the count, number of unique values, the mode (top), and the frequency of the most common value.
        """
        
        description = get_column(self.df, column_name).describe()
        return description
    
    def get_column_median(self, column_name: str) -> float:
        """Returns the median value of the column whose name matches the column_name parameter."""
        median = get_column(self.df, column_name).median()
        return median
    
    def get_column_mean(self, column_name: str, precision=2) -> float:
        """Returns the mean value of the column whose name matches the column_name parameter.
                
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """
        
        mean = get_column(self.df, column_name).mean()
        mean = round(mean, precision)
        return mean
    
    def get_column_mode(self, column_name: str) -> pd.Series:
        """Returns the mode of the column whose name matches the column_name parameter."""
        
        mode = get_column(self.df, column_name).mode()
        return mode
    
    def get_column_standard_deviation(self, column_name: str, precision=2) -> float:
        """Returns the standard deviation of the column whose name matches the column_name parameter.
                
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.    
        """
        
        std = get_column(self.df, column_name).std()
        std = round(std, precision)
        return std
    
    def get_distinct_categories_in_colum(self, column_name: str) -> List:
        """Returns a list of unique values in the given column, if that column is of type 'category'."""

        # This checks if the column exists and assigns it to column
        column = get_column(self.df, column_name)
        
        # This gets the names of the columns which are of type 'category' to ensure the provided column_name column is not of a different type
        category_columns = self.get_categorical_columns().columns
        
        if column_name not in list(category_columns):
            raise Exception(f"The column {column_name} is not of type category.")
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
    
    def count_nulls_in_data_frame(self) -> pd.Series:
        """Returns a series showing the null count for every column in the dataframe."""
        
        null_series = self.df.isnull().sum()
        return null_series
    
    def percentage_of_nulls_in_data_frame(self, precision=2) -> pd.Series:
        """Returns a series showing the percentage of null values for every column in the dataframe.
        
            Args: 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """        
        
        null_percentages = round(self.df.isnull().sum() * 100 / len(self.df), precision)
        return null_percentages

    def count_nulls_in_column(self, column_name: str) -> int:
        """Return the total number of null values in the series."""
        
        column = get_column(self.df, column_name)
        null_count = column.isnull().sum()
        return null_count
    
    def percentage_of_nulls_in_column(self, column_name: str, precision=2) -> float:
        """Return the proportion of null values in the series as a percentage.
        
            Args:
                column_name (str): the name of the column to be accessed 
                precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """
        
        column = get_column(self.df, column_name)
        null_percentage = round(column.isnull().sum() * 100 / len(column), precision)
        return null_percentage