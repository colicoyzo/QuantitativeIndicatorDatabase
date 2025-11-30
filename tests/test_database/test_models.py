"""
Tests for database models
"""

import pytest
from datetime import datetime
from quant_indicator_db.database.models import Indicator, StockData, FundamentalData


def test_indicator_model():
    """Test Indicator model creation"""
    indicator = Indicator(
        name='RSI',
        symbol='TEST',
        value=50.0,
        timestamp=datetime.now(),
        frequency='D'
    )
    
    assert indicator.name == 'RSI'
    assert indicator.symbol == 'TEST'
    assert indicator.value == 50.0
    assert indicator.frequency == 'D'


def test_stock_data_model():
    """Test StockData model creation"""
    stock_data = StockData(
        symbol='TEST',
        date=datetime.now(),
        open_price=100.0,
        high_price=110.0,
        low_price=90.0,
        close_price=105.0,
        volume=1000
    )
    
    assert stock_data.symbol == 'TEST'
    assert stock_data.open_price == 100.0
    assert stock_data.high_price == 110.0
    assert stock_data.low_price == 90.0
    assert stock_data.close_price == 105.0
    assert stock_data.volume == 1000


def test_fundamental_data_model():
    """Test FundamentalData model creation"""
    fundamental_data = FundamentalData(
        symbol='TEST',
        pe_ratio=15.0,
        pb_ratio=2.0,
        dividend_yield=0.03,
        market_cap=1000000000.0,
        total_debt=500000000.0,
        total_equity=500000000.0,
        net_income=100000000.0,
        total_assets=1500000000.0,
        timestamp=datetime.now()
    )
    
    assert fundamental_data.symbol == 'TEST'
    assert fundamental_data.pe_ratio == 15.0
    assert fundamental_data.pb_ratio == 2.0
    assert fundamental_data.dividend_yield == 0.03