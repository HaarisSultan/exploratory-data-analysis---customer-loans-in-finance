import matplotlib.pyplot as plt
import missingno as msno 
import numpy as np
import seaborn as sns

from pandas import DataFrame, Series

from statsmodels.graphics.gofplots import qqplot
from typing import List



class Plotter():
    """A class for generating plots to visualise aspects of a DataFrame. 
    
    Attributes:
        None
        
    Methods:
        plot_histogram_quad: Plots histograms for 4 columns in a quadrant.
        pair_plot: Creates pairwise plot of all columns.
        box_and_whiskers: Plots box and whiskers chart for column.
        plot_box_whiskers_and_histogram: Plots box, whiskers and histogram for column.
        plot_histogram_before_and_after_transform: Plots histograms before and after a transform.
        plot_histogram_and_qq: Plots histogram and Q-Q plot for column.
        qq_plot: Generates Q-Q plot for column data.
        histogram: Plots a histogram for provided data.
        scatter_plot: Generates scatter plot for data.
        correlation_matrix: Computes and plots correlation matrix, and returns the numerical matrix.
        show_null_bar_chart: Generates bar chart showing null values for each column in the DataFrame.
        plot_skew_by_column_name: Plot the skew value for each column in the DataFrame.
                
    """
    def __init__(self):
        print("Loaded Plotter()...")    
        
    def plot_histogram_quad(self, df: DataFrame):
        """Plots histograms for 4 columns in a quadrant."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 8))
        cols = list(df.columns)
                    
        t1 = self.histogram(df[cols[0]], ax=ax1, label="Skew: %.3f"%(df[cols[0]].skew()))  
        t2 = self.histogram(df[cols[1]], ax=ax2, label="Skew: %.3f"%(df[cols[1]].skew()))  
        t3 = self.histogram(df[cols[2]], ax=ax3, label="Skew: %.3f"%(df[cols[2]].skew()))  
        t4 = self.histogram(df[cols[3]], ax=ax4, label="Skew: %.3f"%(df[cols[3]].skew()))  
        
        t1.legend()
        t2.legend()
        t3.legend()
        t4.legend()
        
        plt.tight_layout()
        plt.show()
        
    def pair_plot(self, dataframe: DataFrame):
        """Creates pairwise plot of all columns."""
        return sns.pairplot(dataframe)
    
    def box_and_whiskers(self, column: Series, ax=None):
        """Plots box and whiskers chart for column."""
        if ax is None:
            sns.boxplot(column)
        else:
            sns.boxplot(column, ax=ax)
        
    def plot_box_whiskers_and_histogram(self, column: Series):
        """Plots box, whiskers and histogram for column."""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

        self.box_and_whiskers(column, ax=ax1)  
        self.histogram(column, 15, ax=ax2)
        
        plt.tight_layout()
        plt.show()
        
    def plot_histogram_before_and_after_transform(self, column_before: Series, column_after: Series, transform_name: str):
        """Plots histograms before and after a transform."""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))
        
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
        
    def plot_histogram_and_qq(self, column: Series):
        """Plots histogram and Q-Q plot for column."""

        message = f"Colum: {column.name}, with skew of {round(column.skew(), 3)}."
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

        t1 = self.histogram(column, 15, True, ax=ax1, label="Skew: %.3f"%(column.skew())) 
        t1.legend()
         
        self.qq_plot(column, ax=ax2)
        
        plt.tight_layout()

        return message
    
    def qq_plot(self, column_data: Series, ax=None):
        """Generates Q-Q plot for column data."""

        if ax is None:
            qqplot(column_data , scale=1 ,line='q', fit=True)
        else:
            qqplot(column_data, scale=1, line='q', fit=True, ax=ax)        
        
    def histogram(self, data: Series, bins=15, kde=True, ax=None, label=None):
        """Plots a histogram for provided data."""
        
        if ax is None:
            return sns.histplot(data, bins=bins, kde=kde, label=label)
        else:
            return sns.histplot(data, bins=bins, kde=kde, ax=ax, label=label)
    
    def scatter_plot(self, data: List[float]):
        """Generates scatter plot for data."""
        return sns.scatterplot(data=data)
    
    def barplot(self, data: DataFrame, x: str, y: str):
        return sns.barplot(data, x=x, y=y)
    
    def correlation_matrix(self, data: DataFrame, title: str="Correlation matrix") -> DataFrame:
        """Computes and plots correlation matrix, and returns the numerical matrix."""

        # Compute the correlation matrix
        corr = data.corr()

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool_)
        mask[np.triu_indices_from(mask)] = True

        # set thins up for plotting
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        
        plt.figure(figsize=(10, 8)) 
        plt.yticks(rotation=0)
        plt.title(title)
        
        # Draw the heatmap
        sns.heatmap(corr, mask=mask, square=True, linewidths=.5, annot=True, cmap=cmap, fmt='.2f')
        
        plt.show()
        
        return corr
        
    def show_null_bar_chart(self, dataframe: DataFrame):
        """Generates bar chart showing null values for each column in the DataFrame."""
        return msno.bar(dataframe)
    
    def stacked_bar_plot(self, data: DataFrame, title: str):
        # Plot bar chart
        data.plot(x='Data', kind='bar', stacked=True, title=title)

        plt.show()
    
    # unused
    def plot_skew_by_column_name(self, dataframe: DataFrame, column_name: str):
        """Plot the skew value for each column in the DataFrame, based on the provided column names."""
        # series of skewness for each column
        
        column_data = dataframe[[column_name]]
        
        skew = column_data.skew()[0]
        ax = column_data.plot.kde(bw_method=0.5)
        
        return skew, ax