# Exploratory Data Analysis - Customer Loans in Finance

# Table of contents 
1. [Introduction](#introduction)
1. [Requirements](#requirements)
1. [Installation & Usage](#installation-and-usage)
1. [File structure](#file-structure)
1. [License](#license)

# Introduction 

This is my first time maintaining a reasonably large Data Analytics project. The project performs an exploratory data analysis on a dataset of customer loans. The goal is to gain insights into the data through visualizations and statistical analysis.

Some key points about the project:

- Uses Python libraries like Pandas, Seaborn, and Plotly to wrangle, visualize, and analyze the data
- Follows the typical EDA workflow of data cleaning, exploration, visualization, and analysis
- Outputs visualizations and summary statistics to extract insights and trends from the data

Skills I improved during the project:

- Developed coding skills in Python and Git version control
- Created reusable modules for data transformation and plotting to improve code structure

# Requirements 

To run the Jupyter notebook, you will need:

- Python 3.x
- Jupyter Notebook/Lab installed
- The Python libraries listed in requirements.txt

You can then install the remaining project-specific dependencies using: `pip install -r requirements.txt`

# Installation and Usage 

The main analysis is contained in the Jupyter notebook `EDA.ipynb`. To use:

- Clone this GitHub repository
- Install dependencies listed in requirements.txt
- Run the notebook EDA.ipynb

Key files:

- `data/loan_payments.csv`: Raw loan payment data
- `src/`: EDA.ipynb, the main notebook, and modules containing reuseable code for data transformations, plotting, etc. 

# File structure 
```
.
├── data/
|   └── loan_payments.csv
├── src/
│   ├── data_transform.py 
|   ├── db_utils.py
│   ├── df_information.py
│   ├── df_transform.py
|   ├── EDA.ipynb
│   └── plotter.py
├── .gitignore
├── README.md
└── requirements.txt
```

# License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Copyright (c) 2023 Haaris Sultan

*Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*