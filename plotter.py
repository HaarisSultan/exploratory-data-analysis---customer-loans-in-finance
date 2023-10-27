import numpy as np
import pandas as pd
import seaborn as sns
import missingno as msno 
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from typing import List

class Plotter():
    def __init__(self):
        pass
    
    def facet_grid(self, dataframe: pd.DataFrame, column_names: List[str]):
        sns.set(font_scale=0.7)
        frame = pd.melt(dataframe, value_vars=column_names)
        grid = sns.FacetGrid(frame, col="variable",  col_wrap=3, sharex=False, sharey=False)
        grid = grid.map(sns.histplot, "value", kde=True)
        return grid
        
    
    def histogram(self, data: pd.Series, bins: int, kde=False):
        return sns.histplot(data, bins=bins, kde=kde)
        
    
    def scatter_plot(self, data: List[float]):
        return sns.scatterplot(data=data)
    
    def plot_scatter_matrix(self, dataframe: pd.DataFrame):
        dataframe = dataframe.select_dtypes(include=np.number)
        matrix = scatter_matrix(dataframe, alpha=0.2, figsize=(6, 6), diagonal="kde")
        return matrix
        
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