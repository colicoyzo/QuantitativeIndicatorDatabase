"""
Database Initialization Script
==============================

This script creates the database schema and tables for the quant indicator database.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quant_indicator_db.database.connector import get_connector


def create_database_schema():
    """
    Create database schema and tables
    """
    print("Initializing database...")
    
    try:
        # Get database connector
        db_connector = get_connector()
        
        # Initialize database tables
        if db_connector.initialize_database():
            print("Database initialized successfully!")
        else:
            print("Failed to initialize database")
            return False
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    
    return True


def get_database_ddl(mysql=False):
    """
    Generate DDL statements for the database schema
    
    Args:
        mysql (bool): If True, generate MySQL-compatible DDL
    
    Returns:
        str: SQL DDL statements
    """
    if mysql:
        ddl_statements = """
-- Database Schema DDL for Quantitative Indicator Database (MySQL Version)
-- =======================================================================

-- Table: stock_data
-- Stores historical stock price data
CREATE TABLE stock_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume BIGINT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index on stock_data for faster queries
CREATE INDEX idx_stock_data_symbol_date ON stock_data(symbol, date);


-- Table: indicators
-- Stores calculated indicators
CREATE TABLE indicators (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    value FLOAT NOT NULL,
    timestamp DATETIME NOT NULL,
    frequency VARCHAR(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index on indicators for faster queries
CREATE INDEX idx_indicators_symbol_timestamp ON indicators(symbol, timestamp);


-- Table: fundamental_data
-- Stores fundamental data for stocks
CREATE TABLE fundamental_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    pe_ratio FLOAT,
    pb_ratio FLOAT,
    dividend_yield FLOAT,
    market_cap FLOAT,
    total_debt FLOAT,
    total_equity FLOAT,
    net_income FLOAT,
    total_assets FLOAT,
    timestamp DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index on fundamental_data for faster queries
CREATE INDEX idx_fundamental_data_symbol_timestamp ON fundamental_data(symbol, timestamp);
"""
    else:
        ddl_statements = """
-- Database Schema DDL for Quantitative Indicator Database
-- ======================================================

-- Table: stock_data
-- Stores historical stock price data
CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(20) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume INTEGER
);

-- Index on stock_data for faster queries
CREATE INDEX idx_stock_data_symbol_date ON stock_data(symbol, date);


-- Table: indicators
-- Stores calculated indicators
CREATE TABLE indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    value FLOAT NOT NULL,
    timestamp DATETIME NOT NULL,
    frequency VARCHAR(10) NOT NULL
);

-- Index on indicators for faster queries
CREATE INDEX idx_indicators_symbol_timestamp ON indicators(symbol, timestamp);


-- Table: fundamental_data
-- Stores fundamental data for stocks
CREATE TABLE fundamental_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(20) NOT NULL,
    pe_ratio FLOAT,
    pb_ratio FLOAT,
    dividend_yield FLOAT,
    market_cap FLOAT,
    total_debt FLOAT,
    total_equity FLOAT,
    net_income FLOAT,
    total_assets FLOAT,
    timestamp DATETIME NOT NULL
);

-- Index on fundamental_data for faster queries
CREATE INDEX idx_fundamental_data_symbol_timestamp ON fundamental_data(symbol, timestamp);
"""
    
    return ddl_statements


def save_ddl_to_file(mysql=False):
    """
    Save DDL statements to a file
    
    Args:
        mysql (bool): If True, save MySQL-compatible DDL
    """
    ddl = get_database_ddl(mysql)
    
    if mysql:
        filename = 'database_schema_mysql.sql'
    else:
        filename = 'database_schema.sql'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(ddl)
    
    print(f"Database DDL saved to {filename}")


if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Initialize database schema")
    parser.add_argument("--mysql", action="store_true", 
                        help="Generate MySQL-compatible schema instead of SQLite")
    args = parser.parse_args()
    
    # Create database schema
    if create_database_schema():
        # Save DDL to file
        save_ddl_to_file(args.mysql)
        print("Database setup completed successfully!")
    else:
        print("Database setup failed!")
        sys.exit(1)