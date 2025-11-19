# Data Directory

This directory is for storing data files that will be loaded into Snowflake.

## Supported Formats

- CSV files (`.csv`)
- JSON files (`.json`)
- Parquet files (`.parquet`)
- Excel files (`.xlsx`)

## Usage

Place your data files here and use the `data_loader.py` script to load them into Snowflake tables.

Example:
```python
from scripts.data_loader import DataLoader
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

loader = DataLoader(sf)
loader.load_csv_to_table(
    csv_path='data/your_file.csv',
    table_name='YOUR_TABLE',
    database='YOUR_DATABASE',
    schema='YOUR_SCHEMA'
)
```

## Note

This directory is tracked by git but data files should be added to `.gitignore` if they contain sensitive information.
