"""
Snowflake Connection Module

This module provides utilities for connecting to Snowflake using 
either environment variables or configuration files.
"""

import os
import snowflake.connector
from dotenv import load_dotenv
import yaml
from typing import Optional


class SnowflakeConnector:
    """
    A class to manage Snowflake database connections.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the Snowflake connector.
        
        Args:
            config_file: Path to YAML configuration file (optional)
        """
        self.connection = None
        self.config_file = config_file
        
    def connect_from_env(self):
        """
        Connect to Snowflake using environment variables.
        
        Returns:
            snowflake.connector.connection: Active Snowflake connection
        """
        # Load environment variables from .env file
        load_dotenv()
        
        connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        # Remove None values
        connection_params = {k: v for k, v in connection_params.items() if v is not None}
        
        self.connection = snowflake.connector.connect(**connection_params)
        return self.connection
    
    def connect_from_config(self, config_path: str = 'config/config.yaml'):
        """
        Connect to Snowflake using a YAML configuration file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            snowflake.connector.connection: Active Snowflake connection
        """
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        connection_params = config.get('snowflake', {})
        self.connection = snowflake.connector.connect(**connection_params)
        return self.connection
    
    def execute_query(self, query: str):
        """
        Execute a SQL query on Snowflake.
        
        Args:
            query: SQL query string to execute
            
        Returns:
            list: Query results as list of tuples
        """
        if not self.connection:
            raise ConnectionError("No active connection. Call connect_from_env() or connect_from_config() first.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
    
    def execute_query_df(self, query: str):
        """
        Execute a SQL query and return results as pandas DataFrame.
        
        Args:
            query: SQL query string to execute
            
        Returns:
            pandas.DataFrame: Query results as DataFrame
        """
        if not self.connection:
            raise ConnectionError("No active connection. Call connect_from_env() or connect_from_config() first.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            # Import pandas here to make it optional
            import pandas as pd
            return pd.DataFrame(results, columns=columns)
        finally:
            cursor.close()
    
    def close(self):
        """Close the Snowflake connection."""
        if self.connection:
            self.connection.close()
            self.connection = None


# Example usage
if __name__ == "__main__":
    # Example 1: Connect using environment variables
    sf = SnowflakeConnector()
    try:
        conn = sf.connect_from_env()
        print("Connected to Snowflake successfully!")
        
        # Example query
        results = sf.execute_query("SELECT CURRENT_VERSION()")
        print(f"Snowflake version: {results[0][0]}")
        
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
    finally:
        sf.close()
