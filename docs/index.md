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
│   ├── database/               # Database storage related
│   ├── backtest/               # Backtesting engine module
│   └── utils/                  # Utility functions collection
├── tests/                      # Unit tests directory
├── docs/                       # Documentation materials
├── examples/                   # Sample scripts and demonstration programs
└── scripts/                    # Automation scripts
```

## Modules

### Indicators

The [indicators](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/indicators) module contains implementations of various quantitative trading indicators:

- Technical indicators (e.g., MACD, RSI, Moving Averages)
- Fundamental indicators (e.g., P/E ratio, P/B ratio, ROE, ROA)

### Data

The [data](file:///D:/PythonData/QuantitativeIndicatorDatabase/quant_indicator_db/data) module handles external market data acquisition and internal data processing:

- Data fetching from various sources
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

## Usage Examples

Check the [examples](file:///D:/PythonData/QuantitativeIndicatorDatabase/examples) directory for sample usage scenarios.

## Testing

Run tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](file:///D:/PythonData/QuantitativeIndicatorDatabase/LICENSE) file for details.