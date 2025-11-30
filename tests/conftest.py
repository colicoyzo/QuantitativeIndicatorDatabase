"""
pytest configuration file
"""

import sys
import os
import pytest
import numpy as np
import pandas as pd


# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_price_data():
    """Generate sample price data for testing"""
    np.random.seed(42)  # For reproducible tests
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    prices = 100 + np.cumsum(np.random.randn(100) * 0.1)
    
    return pd.Series(prices, index=dates)


@pytest.fixture
def sample_financial_data():
    """Generate sample financial data for testing"""
    return {
        'symbol': 'TEST',
        'price': 100.0,
        'earnings_per_share': 5.0,
        'book_value_per_share': 20.0,
        'dividend_per_share': 2.0,
        'total_debt': 1000000,
        'total_equity': 2000000,
        'net_income': 500000,
        'total_assets': 3000000
    }