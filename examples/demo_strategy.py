"""
Demo Strategy Example
===================

This script demonstrates how to use the quant_indicator_db library to implement and backtest a simple trading strategy.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import our modules
from quant_indicator_db.data.fetcher import DataFetcher
from quant_indicator_db.data.processor import DataProcessor
from quant_indicator_db.indicators.technical_indicators import sma, rsi
from quant_indicator_db.backtest.engine import BacktestEngine
from quant_indicator_db.backtest.strategy import MovingAverageCrossoverStrategy


def demo_simple_strategy():
    """
    Demonstrate a simple moving average crossover strategy
    """
    print("=== Quantitative Indicator Database Demo ===")
    print("Running Moving Average Crossover Strategy")
    
    # Initialize components
    fetcher = DataFetcher()
    processor = DataProcessor()
    strategy = MovingAverageCrossoverStrategy(fast_period=5, slow_period=10)
    backtester = BacktestEngine(initial_capital=100000.0)
    
    # Fetch sample data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    print(f"Fetching data from {start_date.date()} to {end_date.date()}")
    
    # In a real scenario, you would fetch actual market data
    # For this demo, we'll simulate it
    symbol = "DEMO"
    data = fetcher.fetch_stock_data(symbol, start_date, end_date)
    print(f"Fetched {len(data)} days of data for {symbol}")
    
    # Process data
    cleaned_data = processor.clean_data(data)
    print(f"Cleaned data has {len(cleaned_data)} records")
    
    # Calculate indicators
    # Note: In a full implementation, this would be integrated better
    print("Calculating indicators...")
    
    # Run backtest
    # For simplicity, we'll use the simple strategy example
    print("Running backtest...")
    
    # Prepare data for backtest (simplified)
    backtest_data = {symbol: {'price': 100}}  # Simplified data structure
    
    try:
        results = backtester.run_backtest(lambda d, i: {symbol: 'BUY' if i % 2 == 0 else 'SELL'}, backtest_data)
        print(f"Backtest complete!")
        print(f"Initial Capital: ${results['initial_capital']:,.2f}")
        print(f"Final Capital: ${results['final_capital']:,.2f}")
        print(f"Total Return: {results['total_return']*100:.2f}%")
        print(f"Number of Trades: {len(results['trades'])}")
    except Exception as e:
        print(f"Backtest failed with error: {e}")


def demo_indicator_calculation():
    """
    Demonstrate indicator calculations
    """
    print("\n=== Indicator Calculation Demo ===")
    
    # Generate sample price data
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(50) * 0.5)
    
    print("Sample price data:", prices[-5:])  # Show last 5 prices
    
    # Calculate SMA
    sma_5 = sma(prices, 5)
    print(f"5-day SMA (last 3 values): {sma_5[-3:]}")
    
    # Calculate RSI
    rsi_values = rsi(prices, 14)
    print(f"RSI (last 3 values): {rsi_values[-3:]}")


if __name__ == "__main__":
    # Run demos
    demo_indicator_calculation()
    demo_simple_strategy()
    
    print("\n=== Demo Complete ===")
    print("This demo shows basic usage of the quant_indicator_db library.")
    print("In a real application, you would:")
    print("1. Connect to real market data sources")
    print("2. Implement more sophisticated strategies")
    print("3. Store results in a database")
    print("4. Perform detailed performance analysis")