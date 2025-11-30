"""
Backtesting Engine Module
=======================

This module implements the backtesting engine for quantitative strategies.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class BacktestEngine:
    """
    A backtesting engine for quantitative trading strategies
    """
    
    def __init__(self, initial_capital=100000.0):
        """
        Initialize the backtesting engine
        
        Args:
            initial_capital (float): Initial capital for the backtest
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}  # symbol -> quantity
        self.trades = []  # List of trades
        self.portfolio_values = []  # Portfolio value over time
        self.dates = []  # Corresponding dates
    
    def buy(self, symbol, quantity, price, date):
        """
        Execute a buy order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of shares to buy
            price (float): Purchase price per share
            date (datetime): Date of purchase
        """
        cost = quantity * price
        if cost <= self.current_capital:
            self.current_capital -= cost
            if symbol in self.positions:
                self.positions[symbol] += quantity
            else:
                self.positions[symbol] = quantity
                
            self.trades.append({
                'date': date,
                'symbol': symbol,
                'action': 'BUY',
                'quantity': quantity,
                'price': price,
                'cost': cost
            })
        else:
            raise ValueError("Insufficient capital for this purchase")
    
    def sell(self, symbol, quantity, price, date):
        """
        Execute a sell order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of shares to sell
            price (float): Selling price per share
            date (datetime): Date of sale
        """
        if symbol in self.positions and self.positions[symbol] >= quantity:
            proceeds = quantity * price
            self.current_capital += proceeds
            self.positions[symbol] -= quantity
            
            # Remove symbol from positions if quantity becomes zero
            if self.positions[symbol] == 0:
                del self.positions[symbol]
                
            self.trades.append({
                'date': date,
                'symbol': symbol,
                'action': 'SELL',
                'quantity': quantity,
                'price': price,
                'proceeds': proceeds
            })
        else:
            raise ValueError("Insufficient shares to sell")
    
    def get_portfolio_value(self, current_prices):
        """
        Calculate current portfolio value
        
        Args:
            current_prices (dict): Symbol -> current price mapping
            
        Returns:
            float: Total portfolio value
        """
        position_value = 0
        for symbol, quantity in self.positions.items():
            if symbol in current_prices:
                position_value += quantity * current_prices[symbol]
        
        return self.current_capital + position_value
    
    def record_portfolio_value(self, date, portfolio_value):
        """
        Record portfolio value for a specific date
        
        Args:
            date (datetime): Date of recording
            portfolio_value (float): Portfolio value
        """
        self.dates.append(date)
        self.portfolio_values.append(portfolio_value)
    
    def run_backtest(self, strategy_func, data):
        """
        Run a backtest using a strategy function
        
        Args:
            strategy_func (function): Function that implements the trading strategy
            data (dict): Market data dictionary with symbols as keys
            
        Returns:
            dict: Backtest results
        """
        # This is a simplified backtest loop
        # In a real implementation, this would iterate through historical data
        # and call the strategy function for each time period
        
        for i in range(10):  # Simulate 10 time periods
            # Call strategy function with current data
            signals = strategy_func(data, i)
            
            # Process signals (this is simplified)
            for symbol, action in signals.items():
                if action == 'BUY':
                    # Simplified buy logic
                    price = data.get(symbol, {}).get('price', 100)
                    quantity = 100
                    try:
                        self.buy(symbol, quantity, price, datetime.now())
                    except ValueError:
                        pass  # Not enough capital
                elif action == 'SELL':
                    # Simplified sell logic
                    price = data.get(symbol, {}).get('price', 100)
                    quantity = 100
                    try:
                        self.sell(symbol, quantity, price, datetime.now())
                    except ValueError:
                        pass  # Not enough shares
                        
            # Record portfolio value
            current_prices = {symbol: info.get('price', 100) 
                            for symbol, info in data.items()}
            portfolio_value = self.get_portfolio_value(current_prices)
            self.record_portfolio_value(datetime.now(), portfolio_value)
        
        return self.get_results()
    
    def get_results(self):
        """
        Get backtest results
        
        Returns:
            dict: Backtest results
        """
        total_return = ((self.portfolio_values[-1] / self.initial_capital) - 1) \
                       if self.portfolio_values else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': self.portfolio_values[-1] if self.portfolio_values else self.initial_capital,
            'total_return': total_return,
            'trades': self.trades,
            'portfolio_values': self.portfolio_values
        }