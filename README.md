# SNOWFLAKE

A comprehensive project structure for working with Snowflake Data Warehouse. This repository provides a foundation for managing Snowflake databases, tables, procedures, and data pipelines using Python and SQL.

## Features

- **Python Integration**: Connect to Snowflake using Python with the official connector
- **SQL Scripts Organization**: Well-structured SQL scripts for DDL, DML, views, and procedures
- **Data Loading Utilities**: Python scripts for loading data from various sources (CSV, JSON, etc.)
- **Configuration Management**: Support for both environment variables and YAML configuration
- **Sample Code**: Example scripts and SQL statements to get started quickly

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Credentials**
   ```bash
   cp config/.env.example .env
   # Edit .env with your Snowflake credentials
   ```

3. **Connect to Snowflake**
   ```python
   from scripts.snowflake_connection import SnowflakeConnector
   
   sf = SnowflakeConnector()
   conn = sf.connect_from_env()
   results = sf.execute_query("SELECT CURRENT_VERSION()")
   sf.close()
   ```

## Project Structure

```
SNOWFLAKE/
├── config/              # Configuration files and examples
├── data/                # Data files for loading
├── docs/                # Documentation
├── scripts/             # Python scripts for Snowflake operations
├── sql/                 # SQL scripts organized by type
│   ├── ddl/            # Data Definition Language
│   ├── dml/            # Data Manipulation Language
│   ├── procedures/     # Stored Procedures
│   └── views/          # View definitions
├── .gitignore
├── README.md
└── requirements.txt
```

## Documentation

For detailed setup instructions and usage examples, see [SETUP.md](docs/SETUP.md).

## Key Components

### Python Scripts

- **snowflake_connection.py**: Connection management and query execution
- **data_loader.py**: Data loading utilities for various file formats

### SQL Scripts

- **DDL Scripts**: Database and table creation
- **DML Scripts**: Sample data insertion
- **Views**: Analytical view definitions
- **Procedures**: Stored procedure examples

## Security

- All credential files are excluded via `.gitignore`
- Use environment variables or secure vaults for production
- Never commit sensitive information to the repository

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

This project is open source and available for use in your Snowflake projects.

## Resources

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Python Connector Docs](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [SQL Reference](https://docs.snowflake.com/en/sql-reference.html)