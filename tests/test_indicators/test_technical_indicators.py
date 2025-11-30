"""
Tests for technical indicators module
"""

import pytest
import numpy as np
import pandas as pd
from quant_indicator_db.indicators.technical_indicators import (
    sma, ema, macd, rsi
)


def test_sma():
    """Test Simple Moving Average calculation"""
    data = [1, 2, 3, 4, 5]
    result = sma(data, 3)
    expected = np.array([2.0, 3.0, 4.0])  # (1+2+3)/3, (2+3+4)/3, (3+4+5)/3
    
    assert len(result) == 3
    np.testing.assert_array_almost_equal(result, expected)


def test_sma_insufficient_data():
    """Test SMA with insufficient data"""
    data = [1, 2]
    with pytest.raises(ValueError):
        sma(data, 3)


def test_ema():
    """Test Exponential Moving Average calculation"""
    data = [1, 2, 3, 4, 5]
    result = ema(data, 3)
    
    assert len(result) == 5
    assert result[0] == 1  # First value should equal first data point


def test_macd():
    """Test MACD calculation"""
    data = list(range(1, 30))  # Trending upward data
    macd_line, signal_line, histogram = macd(data)
    
    assert len(macd_line) > 0
    assert len(signal_line) > 0
    assert len(histogram) > 0


def test_rsi():
    """Test RSI calculation"""
    # Create data with clear up and down movements
    data = [10, 11, 12, 11, 10, 9, 8, 9, 10, 11, 12] 
    
    result = rsi(data, 5)
    
    assert len(result) > 0
    # All RSI values should be between 0 and 100
    assert np.all(result >= 0) and np.all(result <= 100)


def test_rsi_insufficient_data():
    """Test RSI with insufficient data"""
    data = [1, 2]
    with pytest.raises(ValueError):
        rsi(data, 5)