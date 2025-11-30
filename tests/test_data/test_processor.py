"""
Tests for data processor module
"""

import pytest
import pandas as pd
import numpy as np
from quant_indicator_db.data.processor import DataProcessor


@pytest.fixture
def data_processor():
    """Create a DataProcessor instance for testing"""
    return DataProcessor()


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [10, 20, 30, np.inf, 50],
        'C': [100, 200, 300, 400, 500]
    })


def test_clean_data(data_processor, sample_data):
    """Test data cleaning"""
    cleaned_data = data_processor.clean_data(sample_data)
    
    assert isinstance(cleaned_data, pd.DataFrame)
    # Check that NaN values are removed
    assert not cleaned_data.isnull().values.any()


def test_normalize_data(data_processor):
    """Test data normalization"""
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    
    normalized_data = data_processor.normalize_data(data)
    
    assert isinstance(normalized_data, pd.DataFrame)
    # Check that values are normalized between 0 and 1
    for column in normalized_data.columns:
        assert normalized_data[column].min() == 0.0
        assert normalized_data[column].max() == 1.0


def test_calculate_returns(data_processor):
    """Test return calculations"""
    price_data = pd.Series([100, 105, 102, 108, 99])
    returns = data_processor.calculate_returns(price_data)
    
    assert isinstance(returns, pd.Series)
    assert len(returns) == len(price_data) - 1
    # Check first return calculation: (105-100)/100 = 0.05
    assert abs(returns.iloc[0] - 0.05) < 1e-10