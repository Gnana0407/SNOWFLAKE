"""
Data Loader Module

This module provides utilities for loading data into Snowflake
from various sources (CSV, JSON, Parquet, etc.)
"""

import pandas as pd
from snowflake_connection import SnowflakeConnector
from typing import Optional


class DataLoader:
    """
    A class to load data into Snowflake tables.
    """
    
    def __init__(self, sf_connector: SnowflakeConnector):
        """
        Initialize the DataLoader with a Snowflake connector.
        
        Args:
            sf_connector: An initialized SnowflakeConnector instance
        """
        self.sf_connector = sf_connector
    
    def load_csv_to_table(self, 
                          csv_path: str, 
                          table_name: str, 
                          database: str,
                          schema: str,
                          if_exists: str = 'append'):
        """
        Load data from CSV file into Snowflake table.
        
        Args:
            csv_path: Path to the CSV file
            table_name: Target table name
            database: Target database name
            schema: Target schema name
            if_exists: How to behave if table exists ('append', 'replace', 'fail')
        """
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Load to Snowflake
        self._load_dataframe_to_table(
            df, table_name, database, schema, if_exists
        )
    
    def load_json_to_table(self,
                          json_path: str,
                          table_name: str,
                          database: str,
                          schema: str,
                          if_exists: str = 'append'):
        """
        Load data from JSON file into Snowflake table.
        
        Args:
            json_path: Path to the JSON file
            table_name: Target table name
            database: Target database name
            schema: Target schema name
            if_exists: How to behave if table exists ('append', 'replace', 'fail')
        """
        # Read JSON file
        df = pd.read_json(json_path)
        
        # Load to Snowflake
        self._load_dataframe_to_table(
            df, table_name, database, schema, if_exists
        )
    
    def _load_dataframe_to_table(self,
                                 df: pd.DataFrame,
                                 table_name: str,
                                 database: str,
                                 schema: str,
                                 if_exists: str = 'append'):
        """
        Load a pandas DataFrame into Snowflake table.
        
        Args:
            df: pandas DataFrame to load
            table_name: Target table name
            database: Target database name
            schema: Target schema name
            if_exists: How to behave if table exists ('append', 'replace', 'fail')
        """
        from snowflake.connector.pandas_tools import write_pandas
        
        if not self.sf_connector.connection:
            raise ConnectionError("No active Snowflake connection")
        
        # Write DataFrame to Snowflake
        success, nchunks, nrows, _ = write_pandas(
            conn=self.sf_connector.connection,
            df=df,
            table_name=table_name,
            database=database,
            schema=schema,
            auto_create_table=True,
            overwrite=(if_exists == 'replace')
        )
        
        if success:
            print(f"Successfully loaded {nrows} rows into {database}.{schema}.{table_name}")
        else:
            print(f"Failed to load data into {database}.{schema}.{table_name}")
    
    def bulk_load_from_stage(self,
                            stage_name: str,
                            file_pattern: str,
                            table_name: str,
                            file_format: str = 'CSV'):
        """
        Bulk load data from a Snowflake stage.
        
        Args:
            stage_name: Name of the Snowflake stage
            file_pattern: File pattern to match (e.g., '*.csv')
            table_name: Target table name
            file_format: File format (CSV, JSON, PARQUET, etc.)
        """
        copy_query = f"""
        COPY INTO {table_name}
        FROM @{stage_name}/{file_pattern}
        FILE_FORMAT = (TYPE = {file_format})
        ON_ERROR = 'CONTINUE'
        """
        
        self.sf_connector.execute_query(copy_query)
        print(f"Bulk load completed for {table_name}")


# Example usage
if __name__ == "__main__":
    # Initialize connector
    sf = SnowflakeConnector()
    sf.connect_from_env()
    
    # Initialize data loader
    loader = DataLoader(sf)
    
    # Example: Load CSV file
    # loader.load_csv_to_table(
    #     csv_path='data/customers.csv',
    #     table_name='CUSTOMERS',
    #     database='MY_DATABASE',
    #     schema='RAW_DATA'
    # )
    
    sf.close()
