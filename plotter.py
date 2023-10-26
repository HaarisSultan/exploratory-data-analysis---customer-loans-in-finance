import numpy as np
import pandas as pd
import seaborn as sns
import missingno as msno 
import matplotlib.pyplot as plt
from typing import List

class Plotter():
    def __init__(self):
        pass
    
    def plot_skew_by_column_name(self, dataframe: pd.DataFrame, column_name: str):
        # series of skewness for each column
        
        column_data = dataframe[[column_name]]
        
        skew = column_data.skew()[0]
        
        ax = self.plot_column_skew(column_data)
        
        return skew, ax
        
    
    def show_null_bar_chart(self, dataframe: pd.DataFrame):
        return msno.bar(dataframe)
        
    def plot_column_skew(self, column: pd.Series):
        ax = column.plot.kde(bw_method=0.5)
        return ax
    
    def correlation_matrix(self, columns: pd.DataFrame):
        
        # Compute the correlation matrix
        corr = columns.corr()

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool_)
        mask[np.triu_indices_from(mask)] = True

        # set thins up for plotting
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap
        sns.heatmap(corr, mask=mask, 
                    square=True, linewidths=.5, annot=False, cmap=cmap)
        plt.yticks(rotation=0)
        plt.title('Correlation Matrix of all Numerical Variables')
        plt.show()