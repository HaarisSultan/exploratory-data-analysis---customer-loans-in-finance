# Exploratory Data Analysis - Customer Loans in Finance

# Table of contents 
1. [Introduction](#introduction)
1. [Installation](#installation)
1. [File structure](#file-structure)
1. [License](#license)

# Introduction 

This is my first time maintaining and working on a Data Analytics project; through it I have been able to develop and consolidate various aspects of my programming skills. For example:

- Working with the pandas library
- Writing clean code; creating multiple classes; using both notebooks and modules.
- Gained more familiarity with Git and GitHub; keeping code up to date with docstrings; and writing a README
- Worked on a Exploratory Data Analysis task to get used to working with large data sets 

The bulk of the code is in the EDA.ipynb file, which is where the data analysis takes place. The other python files (except for `db_utils.py`) provide functions to assist the EDA file in its analysis. 

# File structure 
```
.
├── data_transform.py
├── db_utils.py
├── df_information.py
├── df_transform.py
├── EDA.ipynb
├── plotter.py
├── README.md
└── requirements.txt

```

# Installation 
1. Clone the project to your local machine using `git clone https://github.com/HaarisSultan/exploratory-data-analysis---customer-loans-in-finance.git`
2. Install the dependencies listed in `requirements.txt` using a package manager *(e.g. pip or brew)*

I had to download the `loan_payments.csv` file for the data analysis by running `python db_utils.py` - which only works if you have a credentials.yaml file in the project directory. 

For anyone wishing to run the project without the credentials file, I have simply added the `loan_payments.csv` file to the project, so the db_utils.py file is not needed. 

3. Open the file EDA.ipynb click Run All  

# Licence

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