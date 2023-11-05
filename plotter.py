import missingno as msno 
import numpy as np
import pandas as pd
import seaborn as sns

import plotly.express as px
import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix
from statsmodels.graphics.gofplots import qqplot
from typing import List

class Plotter():
    def __init__(self):
        print("Loaded Plotter()...")    
        
    def plot_hist_quad(self, dataframe: pd.DataFrame):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
        cols = list(dataframe.columns)
        
        self.histogram(dataframe[cols[0]], 20, True, ax=ax1)  
        self.histogram(dataframe[cols[1]], 20, True, ax=ax2)  
        self.histogram(dataframe[cols[2]], 20, True, ax=ax3)  
        self.histogram(dataframe[cols[3]], 20, True, ax=ax4)  
        
        plt.tight_layout()
        plt.show()
        
    def pair_plot(self, dataframe: pd.DataFrame):
        return sns.pairplot(dataframe)
    
    def box_and_whiskers(self, column_data: pd.Series, ax=None):
        
        if ax is None:
            sns.boxplot(column_data)
        else:
            sns.boxplot(column_data, ax=ax)
        
    def plot_box_whiskers_and_hist(self, column_data: pd.Series):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        self.box_and_whiskers(column_data, ax=ax1)  
        self.histogram(column_data, 15, ax=ax2)
        
        plt.tight_layout()
        plt.show()
        
    def plot_hist_before_after_transform(self, column_before: pd.Series, column_after: pd.Series, transform_name: str):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        # Add overall figure title 
        fig.suptitle(f"Change in skew for {column_before.name}, after applying a {transform_name} transformation.", fontsize=12)
        
        ax1.set_xlabel(column_before.name)
        ax2.set_xlabel(column_before.name)
        
        t1 = self.histogram(column_before, ax=ax1, label="Skew before: %.3f"%(column_before.skew()))
        t2 = self.histogram(column_after, ax=ax2, label="Skew after: %.3f"%(column_after.skew()))
        
        t1.legend()
        t2.legend()
            
        plt.tight_layout()
        plt.show()
        
        
    def plot_hist_and_qq(self, column_data: pd.Series):

        message = f"Colum: {column_data.name}, with skew of {round(column_data.skew(), 3)}."
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        self.histogram(column_data, 15, True, ax=ax1)  
        self.qq_plot(column_data, ax=ax2)
        
        plt.tight_layout()

        return message
        
    def facet_grid(self, dataframe: pd.DataFrame, column_names: List[str]):
        sns.set(font_scale=0.7)
        frame = pd.melt(dataframe, value_vars=column_names)
        grid = sns.FacetGrid(frame, col="variable",  col_wrap=3, sharex=False, sharey=False)
        grid = grid.map(sns.histplot, "value", kde=True)
        return grid
    
    def qq_plot(self, column_data: pd.Series, ax=None):
        if ax is None:
            qqplot(column_data , scale=1 ,line='q', fit=True)
        else:
            qqplot(column_data, scale=1, line='q', fit=True, ax=ax)        
        
    def histogram(self, data: pd.Series, bins=15, kde=True, ax=None, label=None):
        if ax is None:
            return sns.histplot(data, bins=bins, kde=kde, label=label)
        else:
            return sns.histplot(data, bins=bins, kde=kde, ax=ax, label=label)
 
    def scatter_outliers(self, original: pd.Series, outliers: pd.Series):
        
        # Plot original data 
        data_df = original.to_frame('values') 
        ax = sns.scatterplot(data=data_df, x=data_df.index, y='values')

        # Overlay outliers in red
        outlier_df = outliers.to_frame('values') 
        ax = sns.scatterplot(data=outlier_df, x=outlier_df.index, y='values', color='red', ax=ax, sizes=(1, 4))

        # Label axes
        ax.set(xlabel='Index', ylabel='Value') 

        # Show plot
        plt.show()
    
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
        ax = self.plot_column_skew_kde(column_data)
        
        return skew, ax
    
    def show_null_bar_chart(self, dataframe: pd.DataFrame):
        return msno.bar(dataframe)
        
    def plot_column_skew_kde(self, column: pd.Series):
        return column.plot.kde(bw_method=0.5)
    
    def corr_matrix(self, columns: pd.DataFrame):
        return px.imshow(columns.corr(), title="Correlation heatmap of dataframe")
    
    def correlation_matrix(self, columns: pd.DataFrame) -> pd.DataFrame:
        
        # Compute the correlation matrix
        corr = columns.corr()

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool_)
        mask[np.triu_indices_from(mask)] = True

        # set thins up for plotting
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        plt.figure(figsize=(10, 8)) 
        # Draw the heatmap
        sns.heatmap(corr, mask=mask, 
                    square=True, linewidths=.5, annot=True, cmap=cmap, fmt='.2g')
        plt.yticks(rotation=0)
        plt.title('Correlation Matrix of all Numerical Variables')
        plt.show()
        return corr