import pandas as pd
import yaml 

from sqlalchemy import Engine, create_engine
from typing import Any

def load_credentials() -> Any:
    """Extract credentials from the yaml file and return its contents as a dict"""

    try:
        with open('credentials.yaml', 'r') as f:
            data = yaml.safe_load(f)
            return data
    except IOError:
        print("IOError: 'credentials.yaml' not found or could not be opened.")
        return None
    
def save_to_csv(dataframe: pd.DataFrame, filepath: str) -> None:
    """Save Pandas DataFrame to a CSV file."""
    
    dataframe.to_csv(filepath, sep=',')

class RDSDatabaseConnector():
    """Connects to an RDS database, extracts data as a DataFrame and saves to CSV.

    Attributes:
        None
    
    Methods:
        __init__(credentials):
            Initializes the RDS engine, extracts data as DF and saves to CSV.
        extract_sql_as_df(engine):
            Uses engine to get SQL data from table as a pandas DataFrame.
        init_SQL_alchemy_engine(credentials):
            Creates SQLAlchemy engine using credentials dict.

    """
    
    def __init__(self, credentials: dict):
        """Initializes the RDS engine, extracts data as DF and saves to CSV"""
        # Get an engine to connect to the SQL database
        engine = self.init_SQL_alchemy_engine(credentials)
        
        # Use the engine to extract data and convert it into a DataFrame
        dataframe = self.extract_table_as_dataframe(engine)
        
        # Save the DataFrame into a csv file
        save_to_csv(dataframe, "loan_payments.csv")
            
    def extract_table_as_dataframe(self, engine: Engine):
        """Extract SQL data and return it as a Pandas DataFrame."""
        
        df = pd.read_sql_table('loan_payments', engine).set_index('id')
        return df

    def init_SQL_alchemy_engine(self, credentials: dict) -> Engine:
        """Use credentials to initialise an SQLAlchemy engine. 

        Args:
            credentials (dict): credentials to connect to an SQLAlchemy database

        Returns:
            engine (Engine): object to allow interaction with the database
        """
        
        # Extract each credential field from the dictionary and format into a connection_url
        HOST = credentials['RDS_HOST']
        PASSWORD = credentials['RDS_PASSWORD']
        DATABASE = credentials['RDS_DATABASE']
        USER = credentials['RDS_USER']
        PORT = credentials['RDS_PORT']

        connection_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        engine = create_engine(connection_url)
        
        return engine 
    
if __name__ == '__main__':
    # Extract connection details into dictionary 
    credentials_dict = load_credentials()
    
    # Use details to connect to the RDSDatabase with the loan data
    RDSDatabaseConnector(credentials_dict)
    