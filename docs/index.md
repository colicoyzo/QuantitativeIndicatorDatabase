# Quantitative Indicator Database Documentation

## Overview

Quantitative Indicator Database is a Python library for calculating, storing, and analyzing quantitative financial indicators. It provides tools for technical and fundamental analysis, data fetching and processing, database storage, and backtesting trading strategies.

## Installation

To install the package, run:

```bash
pip install -r requirements.txt
```

## Project Structure

```
QuantitativeIndicatorDatabase/
├── quant_indicator_db/         # Core source code directory
│   ├── indicators/             # Various quantitative indicator implementations
│   ├── data/                   # Data processing modules
│   │   ├── fetcher.py          # Generic data fetcher
│   │   ├── futu_fetcher.py     # Futu API data fetcher
│   │   └── processor.py        # Data processor
│   ├── database/               # Database storage related
│   ├── backtest/               # Backtesting engine module
│   ├── mcp_service.py          # MCP service for Dify.ai integration
│   └── utils/                  # Utility functions collection
├── tests/                      # Unit tests directory
├── docs/                       # Documentation materials
├── examples/                   # Sample scripts and demonstration programs
└── scripts/                    # Automation scripts
    ├── init_database.py        # Database initialization script
    ├── sync_futu_data.py       # Futu data synchronization script
    ├── update_indicators.py    # Indicator update script
    └── start_mcp_service.py    # MCP service launcher
```

## Modules

### Indicators

The [indicators](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/indicators) module contains implementations of various quantitative trading indicators:

- Technical indicators (e.g., MACD, RSI, Moving Averages)
- Fundamental indicators (e.g., P/E ratio, P/B ratio, ROE, ROA)

### Data

The [data](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/data) module handles external market data acquisition and internal data processing:

- Data fetching from various sources including Futu API
- Data preprocessing and cleaning

### Database

The [database](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/database) module provides database storage functionality:

- ORM models for financial data
- Database connection management

### Backtest

The [backtest](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/backtest) module builds a backtesting framework:

- Backtesting engine
- Strategy templates and examples

### Utils

The [utils](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/utils) module collects reusable utility functions.

### MCP Service

The [mcp_service.py](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/mcp_service.py) module provides a Model Control Protocol service that can be called by Dify.ai platform. It exposes quant indicator functions as API endpoints.

## Usage Examples

Check the [examples](file:///D:/PythonData/QuantitativeIndicatorDatabase/examples) directory for sample usage scenarios.

## Database Schema

The database schema is defined in [database_schema.sql](file:///D:/PythonData/QuantitativeIndicatorDatabase/database_schema.sql) (for SQLite) and [database_schema_mysql.sql](file:///D:/PythonData/QuantitativeIndicatorDatabase/database_schema_mysql.sql) (for MySQL) and includes tables for:

- Stock price data
- Calculated indicators
- Fundamental data

To initialize the database, run:

```bash
python scripts/init_database.py [--mysql]
```

Use the `--mysql` flag to generate MySQL-compatible schema.

## Futu API Integration

To sync data from Futu API:

1. Install Futu API: `pip install futu-api`
2. Start FutuOpenD client
3. Run the sync script:

```bash
python scripts/sync_futu_data.py
```