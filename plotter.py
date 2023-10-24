import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List

class Plotter():
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        
    
    
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