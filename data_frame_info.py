import pandas as pd    

def get_column(dataframe: pd.DataFrame, column_name) -> pd.Series:
    if column_name not in dataframe.columns:
        raise Exception("Error: column name {column_name} is not in the provided DataFrame.")
    else:
        column = pd.Series(dataframe[column_name])
        return column
    
    
class DataFrameInfo():
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_names = df.columns
        
    def describe_all(self):
        description = self.df.describe()
        return description
    
    def show_all_column_dtypes(self):
        return self.df.dtypes

    def describe_column(self, column_name):
        description = get_column(self.df, column_name).describe()
        return description
    
    def get_column_median(self, column_name):
        median = get_column(self.df, column_name).median()
        return median
    
    def get_column_mean(self, column_name):
        mean = get_column(self.df, column_name).mean()
        return mean
    
    def get_column_mode(self, column_name):
        mode = get_column(self.df, column_name).mode()
        return mode
    
    def get_column_standard_deviation(self, column_name):
        std = get_column(self.df, column_name).std()
        return std
    
    # def get_distinct_categories_in_colum(self, column_name):
    #     column = get_column(self.df, column_name)
    #     category_columns = self.get_categorical_columns().columns
    #     if column not in category_columns:
    #         raise Exception(f"The column {column_name} is not of type category.")
    #     else:
    #         # column.
        
    
    def get_categorical_columns(self):
        categorical_cols = self.df.select_dtypes("category")
        return categorical_cols
    
    def print_dataframe_shape(self):
        return self.df.shape


        
"""
    Describe all columns in the DataFrame to check their data types
    Extract statistical values: median, standard deviation and mean from the columns and the DataFrame
    Count distinct values in categorical columns
    Print out the shape of the DataFrame
    Generate a count/percentage count of NULL values in each column
"""