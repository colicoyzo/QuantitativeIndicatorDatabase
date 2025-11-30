"""
Tests for data fetcher module
"""

import pytest
import pandas as pd
from quant_indicator_db.data.fetcher import DataFetcher


@pytest.fixture
def data_fetcher():
    """Create a DataFetcher instance for testing"""
    return DataFetcher()


def test_fetch_stock_data(data_fetcher):
    """Test fetching stock data"""
    data = data_fetcher.fetch_stock_data('TEST', '2020-01-01', '2020-01-31')
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert 'open' in data.columns
    assert 'high' in data.columns
    assert 'low' in data.columns
    assert 'close' in data.columns
    assert 'volume' in data.columns


def test_fetch_fundamental_data(data_fetcher):
    """Test fetching fundamental data"""
    data = data_fetcher.fetch_fundamental_data('TEST')
    
    assert isinstance(data, dict)
    assert 'symbol' in data
    assert 'pe_ratio' in data
    assert 'pb_ratio' in data
    assert 'dividend_yield' in data


def test_fetch_economic_data(data_fetcher):
    """Test fetching economic data"""
    data = data_fetcher.fetch_economic_data('GDP', '2020-01-01', '2020-12-31')
    
    assert isinstance(data, pd.Series)
    assert not data.empty