# Snowflake Project Setup Guide

## Prerequisites

- Python 3.8 or higher
- Snowflake account with appropriate credentials
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gnana0407/SNOWFLAKE.git
cd SNOWFLAKE
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Option 1: Using Environment Variables

1. Copy the example environment file:
```bash
cp config/.env.example .env
```

2. Edit `.env` with your Snowflake credentials:
```
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role
```

### Option 2: Using Configuration File

1. Copy the example config file:
```bash
cp config/config.yaml.example config/config.yaml
```

2. Edit `config/config.yaml` with your Snowflake credentials.

## Project Structure

```
SNOWFLAKE/
├── config/              # Configuration files
│   ├── .env.example
│   └── config.yaml.example
├── data/                # Data files (CSV, JSON, etc.)
├── docs/                # Documentation
│   └── SETUP.md
├── scripts/             # Python scripts
│   ├── snowflake_connection.py
│   └── data_loader.py
├── sql/                 # SQL scripts
│   ├── ddl/            # Data Definition Language
│   ├── dml/            # Data Manipulation Language
│   ├── procedures/     # Stored Procedures
│   └── views/          # Views
├── .gitignore
├── README.md
└── requirements.txt
```

## Usage

### Connecting to Snowflake

```python
from scripts.snowflake_connection import SnowflakeConnector

# Using environment variables
sf = SnowflakeConnector()
conn = sf.connect_from_env()

# Or using config file
conn = sf.connect_from_config('config/config.yaml')

# Execute queries
results = sf.execute_query("SELECT CURRENT_VERSION()")
print(results)

# Close connection
sf.close()
```

### Loading Data

```python
from scripts.snowflake_connection import SnowflakeConnector
from scripts.data_loader import DataLoader

# Initialize connection
sf = SnowflakeConnector()
sf.connect_from_env()

# Initialize data loader
loader = DataLoader(sf)

# Load CSV file
loader.load_csv_to_table(
    csv_path='data/customers.csv',
    table_name='CUSTOMERS',
    database='MY_DATABASE',
    schema='RAW_DATA'
)

sf.close()
```

## Running SQL Scripts

Execute SQL scripts using SnowSQL or through the Python connector:

```bash
# Using SnowSQL
snowsql -f sql/ddl/create_database.sql

# Or using Python
python scripts/snowflake_connection.py
```

## Security Notes

- Never commit credentials to version control
- Use `.env` files for local development (already in .gitignore)
- Use Snowflake key-pair authentication for production
- Rotate credentials regularly

## Troubleshooting

### Connection Issues

1. Verify your Snowflake account identifier
2. Check network connectivity
3. Ensure your IP is whitelisted (if applicable)
4. Verify warehouse is running

### Installation Issues

1. Ensure Python 3.8+ is installed
2. Upgrade pip: `pip install --upgrade pip`
3. Install build tools if needed

## Additional Resources

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowflake Python Connector](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Snowflake Best Practices](https://docs.snowflake.com/en/user-guide/best-practices.html)
