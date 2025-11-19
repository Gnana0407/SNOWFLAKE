# Snowflake Project Examples

This document provides practical examples for common Snowflake operations using this project structure.

## Table of Contents

1. [Basic Connection](#basic-connection)
2. [Executing Queries](#executing-queries)
3. [Loading Data](#loading-data)
4. [Working with DataFrames](#working-with-dataframes)
5. [Running SQL Scripts](#running-sql-scripts)

## Basic Connection

### Using Environment Variables

```python
from scripts.snowflake_connection import SnowflakeConnector

# Create connector instance
sf = SnowflakeConnector()

# Connect using .env file
connection = sf.connect_from_env()

# Verify connection
print("Connected successfully!")

# Always close connection when done
sf.close()
```

### Using Config File

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
connection = sf.connect_from_config('config/config.yaml')

print("Connected successfully!")
sf.close()
```

## Executing Queries

### Simple SELECT Query

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

# Execute query
results = sf.execute_query("SELECT CURRENT_VERSION()")
print(f"Snowflake Version: {results[0][0]}")

# Query with results
query = """
SELECT 
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL
FROM MY_DATABASE.RAW_DATA.CUSTOMERS
LIMIT 10
"""

results = sf.execute_query(query)
for row in results:
    print(row)

sf.close()
```

### Query to DataFrame

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

query = "SELECT * FROM MY_DATABASE.RAW_DATA.CUSTOMERS"
df = sf.execute_query_df(query)

print(df.head())
print(f"Total rows: {len(df)}")

sf.close()
```

## Loading Data

### Load CSV File

```python
from scripts.snowflake_connection import SnowflakeConnector
from scripts.data_loader import DataLoader

# Connect to Snowflake
sf = SnowflakeConnector()
sf.connect_from_env()

# Create data loader
loader = DataLoader(sf)

# Load CSV file
loader.load_csv_to_table(
    csv_path='data/customers.csv',
    table_name='CUSTOMERS',
    database='MY_DATABASE',
    schema='RAW_DATA',
    if_exists='append'  # or 'replace' to overwrite
)

sf.close()
```

### Load JSON File

```python
from scripts.snowflake_connection import SnowflakeConnector
from scripts.data_loader import DataLoader

sf = SnowflakeConnector()
sf.connect_from_env()

loader = DataLoader(sf)

loader.load_json_to_table(
    json_path='data/orders.json',
    table_name='ORDERS',
    database='MY_DATABASE',
    schema='RAW_DATA'
)

sf.close()
```

### Load from Pandas DataFrame

```python
import pandas as pd
from scripts.snowflake_connection import SnowflakeConnector
from scripts.data_loader import DataLoader

# Create sample DataFrame
data = {
    'product_id': [1, 2, 3],
    'product_name': ['Widget A', 'Widget B', 'Gadget C'],
    'price': [99.99, 149.99, 75.00]
}
df = pd.DataFrame(data)

# Connect and load
sf = SnowflakeConnector()
sf.connect_from_env()

loader = DataLoader(sf)
loader._load_dataframe_to_table(
    df=df,
    table_name='PRODUCTS',
    database='MY_DATABASE',
    schema='RAW_DATA',
    if_exists='append'
)

sf.close()
```

## Working with DataFrames

### Data Analysis with Pandas

```python
from scripts.snowflake_connection import SnowflakeConnector
import pandas as pd

sf = SnowflakeConnector()
sf.connect_from_env()

# Get data as DataFrame
query = """
SELECT 
    c.CUSTOMER_ID,
    c.FIRST_NAME,
    c.LAST_NAME,
    COUNT(o.ORDER_ID) as TOTAL_ORDERS,
    SUM(o.ORDER_AMOUNT) as TOTAL_SPENT
FROM MY_DATABASE.RAW_DATA.CUSTOMERS c
LEFT JOIN MY_DATABASE.RAW_DATA.ORDERS o ON c.CUSTOMER_ID = o.CUSTOMER_ID
GROUP BY c.CUSTOMER_ID, c.FIRST_NAME, c.LAST_NAME
"""

df = sf.execute_query_df(query)

# Perform analysis
print("Top 5 customers by spending:")
print(df.nlargest(5, 'TOTAL_SPENT'))

# Calculate statistics
print(f"\nAverage order amount: ${df['TOTAL_SPENT'].mean():.2f}")
print(f"Total customers: {len(df)}")

sf.close()
```

## Running SQL Scripts

### Execute SQL File

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

# Read and execute SQL file
with open('sql/ddl/create_tables.sql', 'r') as file:
    sql_script = file.read()
    
    # Split by semicolons and execute each statement
    statements = sql_script.split(';')
    for statement in statements:
        if statement.strip():
            sf.execute_query(statement)
            print(f"Executed: {statement[:50]}...")

sf.close()
```

### Bulk Operations

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

# Insert multiple rows
insert_query = """
INSERT INTO MY_DATABASE.RAW_DATA.CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL)
VALUES 
    (?, ?, ?, ?),
    (?, ?, ?, ?)
"""

# Execute with parameters
cursor = sf.connection.cursor()
cursor.execute(insert_query, (
    4, 'Alice', 'Williams', 'alice@example.com',
    5, 'Charlie', 'Brown', 'charlie@example.com'
))

sf.close()
```

## Error Handling

### Robust Connection with Error Handling

```python
from scripts.snowflake_connection import SnowflakeConnector

def safe_query_execution(query):
    sf = SnowflakeConnector()
    
    try:
        # Connect
        sf.connect_from_env()
        print("Connected to Snowflake")
        
        # Execute query
        results = sf.execute_query(query)
        print(f"Query executed successfully. Rows returned: {len(results)}")
        
        return results
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
        
    finally:
        # Always close connection
        sf.close()
        print("Connection closed")

# Use the function
results = safe_query_execution("SELECT COUNT(*) FROM MY_DATABASE.RAW_DATA.CUSTOMERS")
```

## Advanced Examples

### Transaction Management

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

try:
    # Start transaction
    sf.execute_query("BEGIN TRANSACTION")
    
    # Multiple operations
    sf.execute_query("UPDATE MY_DATABASE.RAW_DATA.CUSTOMERS SET UPDATED_DATE = CURRENT_TIMESTAMP()")
    sf.execute_query("INSERT INTO MY_DATABASE.RAW_DATA.AUDIT_LOG VALUES (...)")
    
    # Commit transaction
    sf.execute_query("COMMIT")
    print("Transaction completed successfully")
    
except Exception as e:
    # Rollback on error
    sf.execute_query("ROLLBACK")
    print(f"Transaction rolled back: {str(e)}")
    
finally:
    sf.close()
```

### Using Stored Procedures

```python
from scripts.snowflake_connection import SnowflakeConnector

sf = SnowflakeConnector()
sf.connect_from_env()

# Call stored procedure
call_query = """
CALL MY_DATABASE.RAW_DATA.UPDATE_CUSTOMER(
    1,
    'newemail@example.com',
    '555-9999'
)
"""

result = sf.execute_query(call_query)
print(f"Procedure result: {result}")

sf.close()
```

## Best Practices

1. **Always close connections**: Use try-finally blocks or context managers
2. **Use parameterized queries**: Prevent SQL injection
3. **Handle errors gracefully**: Wrap database operations in try-except blocks
4. **Use connection pooling**: For applications with many concurrent operations
5. **Monitor query performance**: Use Snowflake query history and profiling tools
6. **Optimize data loading**: Use bulk loading methods for large datasets
