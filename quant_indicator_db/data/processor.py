"""
Data Processor Module
====================

This module handles data preprocessing and cleaning operations.
"""

import pandas as pd
import numpy as np


class DataProcessor:
    """
    A class to preprocess and clean financial data
    """
    
    def __init__(self):
        """
        Initialize the DataProcessor
        """
        pass
    
    def clean_data(self, data):
        """
        Clean data by removing NaN values and outliers
        
        Args:
            data (pd.DataFrame): Raw data
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        # Remove rows with NaN values
        cleaned_data = data.dropna()
        
        # Remove outliers using IQR method (simplified)
        for column in cleaned_data.select_dtypes(include=[np.number]).columns:
            Q1 = cleaned_data[column].quantile(0.25)
            Q3 = cleaned_data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            cleaned_data = cleaned_data[
                (cleaned_data[column] >= lower_bound) & 
                (cleaned_data[column] <= upper_bound)
            ]
            
        return cleaned_data
    
    def normalize_data(self, data):
        """
        Normalize data using min-max scaling
        
        Args:
            data (pd.DataFrame): Data to normalize
            
        Returns:
            pd.DataFrame: Normalized data
        """
        normalized_data = data.copy()
        for column in normalized_data.select_dtypes(include=[np.number]).columns:
            min_val = normalized_data[column].min()
            max_val = normalized_data[column].max()
            if max_val != min_val:  # Avoid division by zero
                normalized_data[column] = (
                    (normalized_data[column] - min_val) / (max_val - min_val)
                )
                
        return normalized_data
    
    def resample_data(self, data, frequency):
        """
        Resample time series data to a different frequency
        
        Args:
            data (pd.DataFrame): Time series data
            frequency (str): Target frequency ('D', 'W', 'M', etc.)
            
        Returns:
            pd.DataFrame: Resampled data
        """
        resampled = data.resample(frequency).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        
        return resampled
    
    def calculate_returns(self, price_data, period=1):
        """
        Calculate returns from price data
        
        Args:
            price_data (pd.Series): Price data
            period (int): Period for return calculation (default: 1)
            
        Returns:
            pd.Series: Returns
        """
        returns = price_data.pct_change(periods=period).dropna()
        return returns