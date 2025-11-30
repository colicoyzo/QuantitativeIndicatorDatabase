"""
Strategy Module
==============

This module provides strategy templates and example strategies for backtesting.
"""

import pandas as pd
import numpy as np


class Strategy:
    """
    Base strategy class
    """
    
    def __init__(self, name):
        """
        Initialize the strategy
        
        Args:
            name (str): Strategy name
        """
        self.name = name
    
    def generate_signals(self, data):
        """
        Generate trading signals based on input data
        
        Args:
            data (pd.DataFrame): Market data
            
        Returns:
            dict: Signals for different symbols
        """
        raise NotImplementedError("generate_signals method must be implemented in subclass")


class MovingAverageCrossoverStrategy(Strategy):
    """
    Moving Average Crossover Strategy
    Buys when fast MA crosses above slow MA, sells when fast MA crosses below slow MA
    """
    
    def __init__(self, fast_period=10, slow_period=20):
        """
        Initialize the strategy
        
        Args:
            fast_period (int): Fast moving average period
            slow_period (int): Slow moving average period
        """
        super().__init__("MovingAverageCrossover")
        self.fast_period = fast_period
        self.slow_period = slow_period
    
    def generate_signals(self, data):
        """
        Generate signals based on moving average crossover
        
        Args:
            data (dict): Dictionary with symbol as key and price data as value
            
        Returns:
            dict: Trading signals
        """
        signals = {}
        
        for symbol, df in data.items():
            if len(df) < self.slow_period:
                continue
                
            # Calculate moving averages
            fast_ma = df['close'].rolling(window=self.fast_period).mean()
            slow_ma = df['close'].rolling(window=self.slow_period).mean()
            
            # Check for crossover
            if len(fast_ma) >= 2 and len(slow_ma) >= 2:
                # If fast MA crossed above slow MA, generate buy signal
                if fast_ma.iloc[-2] <= slow_ma.iloc[-2] and fast_ma.iloc[-1] > slow_ma.iloc[-1]:
                    signals[symbol] = 'BUY'
                # If fast MA crossed below slow MA, generate sell signal
                elif fast_ma.iloc[-2] >= slow_ma.iloc[-2] and fast_ma.iloc[-1] < slow_ma.iloc[-1]:
                    signals[symbol] = 'SELL'
                    
        return signals


class RSIStrategy(Strategy):
    """
    RSI Strategy
    Buys when RSI crosses below 30 (oversold), sells when RSI crosses above 70 (overbought)
    """
    
    def __init__(self, period=14, oversold=30, overbought=70):
        """
        Initialize the strategy
        
        Args:
            period (int): RSI period
            oversold (int): Oversold threshold
            overbought (int): Overbought threshold
        """
        super().__init__("RSIStrategy")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data):
        """
        Generate signals based on RSI levels
        
        Args:
            data (dict): Dictionary with symbol as key and price data as value
            
        Returns:
            dict: Trading signals
        """
        signals = {}
        
        for symbol, df in data.items():
            if len(df) < self.period + 1:
                continue
            
            # Calculate RSI
            deltas = df['close'].diff()
            gains = deltas.where(deltas > 0, 0)
            losses = -deltas.where(deltas < 0, 0)
            
            avg_gain = gains.rolling(window=self.period).mean()
            avg_loss = losses.rolling(window=self.period).mean()
            
            rs = avg_gain / (avg_loss + 1e-10)  # Adding small value to avoid division by zero
            rsi = 100 - (100 / (1 + rs))
            
            # Check for RSI thresholds
            if len(rsi) >= 2:
                # If RSI crossed below oversold level, generate buy signal
                if rsi.iloc[-2] >= self.oversold and rsi.iloc[-1] < self.oversold:
                    signals[symbol] = 'BUY'
                # If RSI crossed above overbought level, generate sell signal
                elif rsi.iloc[-2] <= self.overbought and rsi.iloc[-1] > self.overbought:
                    signals[symbol] = 'SELL'
                    
        return signals


def simple_strategy_example(data, period):
    """
    Simple example strategy for demonstration
    
    Args:
        data (dict): Market data
        period (int): Current period
        
    Returns:
        dict: Trading signals
    """
    signals = {}
    for symbol in data.keys():
        # Simple logic: alternate between BUY and SELL
        if period % 2 == 0:
            signals[symbol] = 'BUY'
        else:
            signals[symbol] = 'SELL'
    return signals