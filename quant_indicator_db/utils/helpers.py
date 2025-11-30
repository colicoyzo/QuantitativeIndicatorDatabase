"""
Utility Functions Module
======================

This module contains helper functions used across the quant indicator database project.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def annualize_returns(returns, periods_per_year=252):
    """
    Annualize returns based on periodic returns
    
    Args:
        returns (float or array-like): Periodic returns
        periods_per_year (int): Number of periods per year (252 for daily, 12 for monthly, etc.)
        
    Returns:
        float or np.array: Annualized returns
    """
    return (1 + returns) ** periods_per_year - 1


def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
    """
    Calculate Sharpe ratio
    
    Args:
        returns (array-like): Periodic returns
        risk_free_rate (float): Risk-free rate (annualized)
        periods_per_year (int): Number of periods per year
        
    Returns:
        float: Sharpe ratio
    """
    if len(returns) == 0:
        return 0.0
        
    # Convert annual risk-free rate to periodic rate
    periodic_risk_free = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    
    # Calculate excess returns
    excess_returns = returns - periodic_risk_free
    
    # Calculate Sharpe ratio
    if np.std(excess_returns) == 0:
        return 0.0
        
    sharpe = np.mean(excess_returns) / np.std(excess_returns)
    
    # Annualize Sharpe ratio
    return sharpe * np.sqrt(periods_per_year)


def max_drawdown(cumulative_returns):
    """
    Calculate maximum drawdown
    
    Args:
        cumulative_returns (array-like): Cumulative returns over time
        
    Returns:
        float: Maximum drawdown
    """
    if len(cumulative_returns) == 0:
        return 0.0
    
    # Calculate running maximum
    running_max = np.maximum.accumulate(cumulative_returns)
    
    # Calculate drawdown
    drawdown = (cumulative_returns - running_max) / (running_max + 1e-10)
    
    # Return maximum drawdown
    return np.min(drawdown)


def normalize_to_range(values, min_val=0, max_val=1):
    """
    Normalize values to a specific range
    
    Args:
        values (array-like): Values to normalize
        min_val (float): Minimum value of target range
        max_val (float): Maximum value of target range
        
    Returns:
        np.array: Normalized values
    """
    values = np.array(values)
    if np.max(values) == np.min(values):
        return np.full_like(values, (min_val + max_val) / 2)
        
    normalized = (values - np.min(values)) / (np.max(values) - np.min(values))
    return normalized * (max_val - min_val) + min_val


def format_currency(amount):
    """
    Format amount as currency string
    
    Args:
        amount (float): Amount to format
        
    Returns:
        str: Formatted currency string
    """
    return f"${amount:,.2f}"


def business_days_between(start_date, end_date):
    """
    Calculate number of business days between two dates
    
    Args:
        start_date (datetime or str): Start date
        end_date (datetime or str): End date
        
    Returns:
        int: Number of business days
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
    # Simplified business day calculation (Monday-Friday)
    day_generator = (start_date + timedelta(x + 1) 
                    for x in range((end_date - start_date).days))
    business_days = sum(1 for day in day_generator if day.weekday() < 5)
    
    return business_days


def get_current_time():
    """
    Get current time formatted as string
    
    Returns:
        str: Current time in 'YYYY-MM-DD HH:MM:SS' format
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')