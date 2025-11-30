"""
Database Models Module
=====================

This module defines the ORM models for the quantitative indicator database.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Indicator(Base):
    """
    Model representing a calculated indicator
    """
    __tablename__ = 'indicators'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    frequency = Column(String(10), nullable=False)  # e.g., 'D' for daily, 'W' for weekly
    
    __table_args__ = (Index('idx_indicators_symbol_timestamp', 'symbol', 'timestamp'),)
    
    def __repr__(self):
        return f"<Indicator(name='{self.name}', symbol='{self.symbol}', value={self.value})>"


class StockData(Base):
    """
    Model representing stock price data
    """
    __tablename__ = 'stock_data'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    
    __table_args__ = (Index('idx_stock_data_symbol_date', 'symbol', 'date'),)
    
    def __repr__(self):
        return f"<StockData(symbol='{self.symbol}', date='{self.date}')>"


class FundamentalData(Base):
    """
    Model representing fundamental data for stocks
    """
    __tablename__ = 'fundamental_data'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    market_cap = Column(Float)
    total_debt = Column(Float)
    total_equity = Column(Float)
    net_income = Column(Float)
    total_assets = Column(Float)
    timestamp = Column(DateTime, nullable=False)
    
    __table_args__ = (Index('idx_fundamental_data_symbol_timestamp', 'symbol', 'timestamp'),)
    
    def __repr__(self):
        return f"<FundamentalData(symbol='{self.symbol}')>"