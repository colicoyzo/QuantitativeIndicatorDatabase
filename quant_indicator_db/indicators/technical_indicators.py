"""
Technical Indicators Module
==========================

This module contains implementations of various technical indicators commonly used in quantitative trading.
"""

import numpy as np
import pandas as pd


def sma(data, period):
    """
    Simple Moving Average
    
    Args:
        data (list or np.array): Price data
        period (int): Number of periods
        
    Returns:
        np.array: SMA values
    """
    if len(data) < period:
        raise ValueError("Not enough data points for the specified period")
    
    return np.convolve(data, np.ones(period)/period, mode='valid')


def ema(data, period):
    """
    Exponential Moving Average
    
    Args:
        data (list or np.array): Price data
        period (int): Number of periods
        
    Returns:
        np.array: EMA values
    """
    if len(data) < period:
        raise ValueError("Not enough data points for the specified period")
        
    alpha = 2 / (period + 1)
    ema_values = np.zeros(len(data))
    ema_values[0] = data[0]
    
    for i in range(1, len(data)):
        ema_values[i] = alpha * data[i] + (1 - alpha) * ema_values[i-1]
        
    return ema_values


def macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Moving Average Convergence Divergence
    
    Args:
        data (list or np.array): Price data
        fast_period (int): Fast EMA period (default: 12)
        slow_period (int): Slow EMA period (default: 26)
        signal_period (int): Signal line period (default: 9)
        
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    fast_ema = ema(data, fast_period)
    # Align slow EMA with fast EMA
    slow_ema = ema(data[len(data)-len(fast_ema):], slow_period)
    
    # Calculate MACD line
    macd_line = fast_ema[-len(slow_ema):] - slow_ema
    
    # Calculate signal line
    signal_line = ema(macd_line, signal_period)
    
    # Calculate histogram
    histogram = macd_line[-len(signal_line):] - signal_line
    
    return macd_line[-len(signal_line):], signal_line, histogram


def macd_sensitive(data, fast_period=8, slow_period=17, signal_period=9):
    """
    Sensitive Moving Average Convergence Divergence
    Uses shorter periods to make the indicator more responsive to price changes
    
    Args:
        data (list or np.array): Price data
        fast_period (int): Fast EMA period (default: 8, shorter than standard 12)
        slow_period (int): Slow EMA period (default: 17, shorter than standard 26)
        signal_period (int): Signal line period (default: 9, same as standard)
        
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    return macd(data, fast_period, slow_period, signal_period)


def rsi(data, period=14):
    """
    Relative Strength Index
    
    Args:
        data (list or np.array): Price data
        period (int): Number of periods (default: 14)
        
    Returns:
        np.array: RSI values
    """
    if len(data) < period + 1:
        raise ValueError("Not enough data points for the specified period")
        
    deltas = np.diff(data)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = np.zeros_like(gains)
    avg_losses = np.zeros_like(losses)
    
    avg_gains[period-1] = np.mean(gains[:period])
    avg_losses[period-1] = np.mean(losses[:period])
    
    for i in range(period, len(gains)):
        avg_gains[i] = (avg_gains[i-1] * (period - 1) + gains[i]) / period
        avg_losses[i] = (avg_losses[i-1] * (period - 1) + losses[i]) / period
    
    rs = avg_gains / (avg_losses + 1e-10)  # Adding small value to avoid division by zero
    rsi_values = 100 - (100 / (1 + rs))
    
    return rsi_values[period-1:]