import pandas as pd    
import numpy as np
from typing import List

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

    def __init__(self):
        # Give the methods access to the dataframe to avoid extensive use of parameters 
        print("Loaded DataFrameInfo()...")

    def measure_skew_for_all_columns(self, dataframe: pd.DataFrame, sort=False) -> pd.Series:
        """Return a series showing the skew value for each column in the dataframe."""
        
        skewness = dataframe.skew(numeric_only=True)
        
        if not sort:
            return skewness

        return skewness.sort_values(ascending=False) 
    
    def print_null_removal_progress(self, dataframe: pd.DataFrame) -> (str, pd.DataFrame): 
        """Display a dataframe containing the null percentage and null count for each column in the dataframe, along with a progress message."""
        
        # Extract only those columns with null values
        columns_with_nulls = self.get_columns_with_nulls(dataframe)

        # This displays both the # and % of nulls in the columns with nulls, good for debugging and tracking progress 
        null_info = self.combine_null_percentage_and_count(columns_with_nulls)
        
        message = f"I have {len(null_info)} columns to deal with:\n"
        
        return message, null_info
        
    def combine_null_percentage_and_count(self, columns: pd.DataFrame) -> pd.DataFrame:
        """Return a dataframe containing the null percentage and null count for each column in the dataframe."""
        
        # Create two series objects containing the count and percentage of nulls in those columns 
        percent_of_nulls = self.percentage_of_nulls_in_data_frame(dataframe=columns, sort=True)
        
        number_of_nulls = self.count_nulls_in_data_frame(dataframe=columns)
        
        # Combine that data to display a DataFrame 
        data = {
            "% of nulls": percent_of_nulls,
            "# of nulls": number_of_nulls,
            "dtype": columns.dtypes
        }
   
        return pd.concat(data, axis=1)      

    def contains_nulls(self, column: pd.Series) -> bool:
        return column.isnull().sum() != 0
    
    def get_z_scores(self, column: pd.Series) -> pd.Series:
        mean = column.mean()
        std = column.std(ddof=0)
         
        return (column - mean) / std
    
    def get_outliers_from_z_score(self, column: pd.Series, threshold=3):
        # Calculate mean and standard deviation  
        z_scores = self.get_z_scores(column)

        # Define outliers as points with z-score outside +/- 3
        return column[np.abs(z_scores) > threshold]
    
    def get_numeric_columns_from_df(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.select_dtypes(include=[np.number]) 
    
    def get_columns_with_nulls(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Returns a DataFrame containing only columns which have null values."""
        return dataframe.loc[:, dataframe.isna().any()]
    
    def describe_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns the count, mean, std, 25%/50%/75% quartiles, and maximum for every column, as a DataFrame."""
        return df.describe()
    
    def show_all_column_dtypes(self, df: pd.DataFrame) -> pd.Series:
        """Returns a Series of data types indexed with the column names."""
        return df.dtypes

    def describe_column(self, column: pd.Series) -> pd.Series:
        """For numerical columns, this returns the count, mean, std, 25%/50%/75% quartiles, and maximum for the given column, as a Series.
        
        For other types, it will return the count, number of unique values, the mode (top), and the frequency of the most common value.
        """
        return column.describe()
    
    def get_column_median(self, column: pd.Series) -> float:
        """Returns the median value of the column whose name matches the column_name parameter."""
        return column.median()
    
    def get_column_mean(self, column: pd.Series, precision=2) -> float:
        """Returns the mean value of the column whose name matches the column_name parameter.
                
        Args: 
            precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
        """
        return round(column.mean(), precision)
    
    def get_column_mode(self, column: pd.Series) -> pd.Series:
        """Returns the mode of the column whose name matches the column_name parameter."""
        return column.mode()
    
    def get_column_standard_deviation(self, column: pd.Series, precision=2) -> float:
        """Returns the standard deviation of the column whose name matches the column_name parameter.
                
        Args: 
            precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.    
        """
        return round(column.std(), precision)
    
    def get_distinct_categories_in_colum(self, column: pd.Series) -> List:
        """Returns a list of unique values in the given column, if that column is of type 'category'."""
        
        # This gets the names of the columns which are of type 'category' to ensure the provided column_name column is not of a different type
        category_columns_list = list(self.get_categorical_columns().columns)
        
        if column.name not in category_columns_list:
            raise Exception(f"The column {column.name} is not of type category.")
        else:
            return list(column.unique())
        
    def get_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts only the columns of the DataFrame whose type is 'category'."""
        return df.select_dtypes("category")
    
    def print_dataframe_shape(self, df: pd.DataFrame) -> tuple[int, int]:
        """Returns the shape of the DataFrame."""
        return df.shape
    
    def count_nulls_in_data_frame(self, dataframe: pd.DataFrame) -> pd.Series:
        """Returns a series showing the null count for every column in the dataframe."""
        return dataframe.isnull().sum()
    
    def percentage_of_nulls_in_data_frame(self, dataframe: pd.DataFrame, precision=2, sort=True) -> pd.Series:
        """Returns a series showing the percentage of null values for every column in the dataframe.
        
        Args: 
            precision (int): the number of values after decimal place to round the percentage to. If none is given it defaults to 2.
            dataframe: dataframe to find the null percentages of 
            sort: whether to return results in ascending order or unsorted 
        """        
        
        null_percentages = round(dataframe.isnull().sum() * 100 / len(dataframe), precision)
        
        if not sort:
            return null_percentages
        else:
            return null_percentages.sort_values(ascending=False)
        
    def count_nulls_in_column(self, column: pd.Series) -> int:
        """Return the total number of null values in the series."""
        return column.isnull().sum()
    
    def show_value_counts(self, column: pd.Series):
        return column.value_counts()
    
    def percentage_of_nulls_in_column(self, column: pd.Series, precision=2) -> float:
        """Return the proportion of null values in the series as a percentage.
        """
        return round(column.isnull().sum() * 100 / len(column), precision)
          
    # unused
    def print_skew_and_dtype(self, dataframe: pd.DataFrame):
        
        skew_series = dataframe.skew(numeric_only=True).sort_values(ascending=False)
        
        columns = dataframe[list(skew_series.index)]
        
        data = {
            "skewness": skew_series,
            "dtype": columns.dtypes
        }
        
        combo = pd.concat(data, axis=1)      
        return combo