-- Database Schema DDL for Quantitative Indicator Database (MySQL Version)
-- =======================================================================
use qiabdb;
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