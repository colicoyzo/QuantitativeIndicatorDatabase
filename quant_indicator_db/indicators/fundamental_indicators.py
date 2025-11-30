"""
Fundamental Indicators Module
============================

This module contains implementations of various fundamental indicators used in quantitative analysis.
"""

import numpy as np
import pandas as pd


def price_to_earnings(price, earnings_per_share):
    """
    Price to Earnings Ratio (P/E)
    
    Args:
        price (float or array-like): Current stock price(s)
        earnings_per_share (float or array-like): Earnings per share
        
    Returns:
        float or np.array: P/E ratio(s)
    """
    if isinstance(earnings_per_share, (int, float)) and earnings_per_share == 0:
        raise ValueError("Earnings per share cannot be zero")
        
    return price / earnings_per_share


def price_to_book(price, book_value_per_share):
    """
    Price to Book Ratio (P/B)
    
    Args:
        price (float or array-like): Current stock price(s)
        book_value_per_share (float or array-like): Book value per share
        
    Returns:
        float or np.array: P/B ratio(s)
    """
    if isinstance(book_value_per_share, (int, float)) and book_value_per_share == 0:
        raise ValueError("Book value per share cannot be zero")
        
    return price / book_value_per_share


def dividend_yield(dividend_per_share, price):
    """
    Dividend Yield
    
    Args:
        dividend_per_share (float or array-like): Annual dividend per share
        price (float or array-like): Current stock price(s)
        
    Returns:
        float or np.array: Dividend yield(s)
    """
    if isinstance(price, (int, float)) and price == 0:
        raise ValueError("Price cannot be zero")
        
    return dividend_per_share / price


def debt_to_equity(total_debt, total_equity):
    """
    Debt to Equity Ratio
    
    Args:
        total_debt (float or array-like): Total debt
        total_equity (float or array-like): Total equity
        
    Returns:
        float or np.array: Debt to equity ratio(s)
    """
    if isinstance(total_equity, (int, float)) and total_equity == 0:
        raise ValueError("Total equity cannot be zero")
        
    return total_debt / total_equity


def roe(net_income, total_equity):
    """
    Return on Equity (ROE)
    
    Args:
        net_income (float or array-like): Net income
        total_equity (float or array-like): Total equity
        
    Returns:
        float or np.array: ROE values
    """
    if isinstance(total_equity, (int, float)) and total_equity == 0:
        raise ValueError("Total equity cannot be zero")
        
    return net_income / total_equity


def roa(net_income, total_assets):
    """
    Return on Assets (ROA)
    
    Args:
        net_income (float or array-like): Net income
        total_assets (float or array-like): Total assets
        
    Returns:
        float or np.array: ROA values
    """
    if isinstance(total_assets, (int, float)) and total_assets == 0:
        raise ValueError("Total assets cannot be zero")
        
    return net_income / total_assets