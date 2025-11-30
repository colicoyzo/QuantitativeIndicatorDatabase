"""
Update Indicators Script
======================

This script updates indicator data in the database.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quant_indicator_db.data.fetcher import DataFetcher
from quant_indicator_db.data.processor import DataProcessor
from quant_indicator_db.indicators.technical_indicators import sma, ema, macd, rsi
from quant_indicator_db.indicators.fundamental_indicators import price_to_earnings, roe, roa
from quant_indicator_db.database.connector import get_connector
from quant_indicator_db.database.models import Indicator, StockData, FundamentalData


def update_technical_indicators(symbols, days=30):
    """
    Update technical indicators for a list of symbols
    
    Args:
        symbols (list): List of stock symbols
        days (int): Number of days of historical data to process
    """
    print(f"Updating technical indicators for {len(symbols)} symbols")
    
    # Initialize components
    fetcher = DataFetcher()
    processor = DataProcessor()
    db_connector = get_connector()
    session = db_connector.get_session()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        for symbol in symbols:
            print(f"Processing {symbol}...")
            
            # Fetch data
            try:
                raw_data = fetcher.fetch_stock_data(symbol, start_date, end_date)
                data = processor.clean_data(raw_data)
                
                if len(data) < 14:  # Need at least 14 days for some indicators
                    print(f"Not enough data for {symbol}, skipping...")
                    continue
                    
                # Calculate indicators
                prices = data['close'].values
                
                # SMA
                if len(prices) >= 20:
                    sma_20 = sma(prices, 20)
                    if len(sma_20) > 0:
                        indicator = Indicator(
                            name='SMA_20',
                            symbol=symbol,
                            value=float(sma_20[-1]),
                            timestamp=end_date,
                            frequency='D'
                        )
                        session.add(indicator)
                
                # RSI
                if len(prices) >= 15:
                    rsi_values = rsi(prices, 14)
                    if len(rsi_values) > 0:
                        indicator = Indicator(
                            name='RSI_14',
                            symbol=symbol,
                            value=float(rsi_values[-1]),
                            timestamp=end_date,
                            frequency='D'
                        )
                        session.add(indicator)
                        
                print(f"Updated indicators for {symbol}")
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        # Commit all changes
        session.commit()
        print("Successfully updated technical indicators")
        
    except Exception as e:
        session.rollback()
        print(f"Error updating technical indicators: {e}")
        
    finally:
        session.close()


def update_fundamental_indicators(symbols):
    """
    Update fundamental indicators for a list of symbols
    
    Args:
        symbols (list): List of stock symbols
    """
    print(f"Updating fundamental indicators for {len(symbols)} symbols")
    
    # Initialize components
    fetcher = DataFetcher()
    db_connector = get_connector()
    session = db_connector.get_session()
    
    try:
        for symbol in symbols:
            print(f"Processing fundamental data for {symbol}...")
            
            try:
                # Fetch fundamental data
                fund_data = fetcher.fetch_fundamental_data(symbol)
                
                # Store in database
                fundamental_record = FundamentalData(
                    symbol=symbol,
                    pe_ratio=fund_data.get('pe_ratio'),
                    pb_ratio=fund_data.get('pb_ratio'),
                    dividend_yield=fund_data.get('dividend_yield'),
                    market_cap=fund_data.get('market_cap'),
                    total_debt=fund_data.get('total_debt'),
                    total_equity=fund_data.get('total_equity'),
                    net_income=fund_data.get('net_income'),
                    total_assets=fund_data.get('total_assets'),
                    timestamp=datetime.now()
                )
                
                session.add(fundamental_record)
                print(f"Updated fundamental data for {symbol}")
                
            except Exception as e:
                print(f"Error processing fundamental data for {symbol}: {e}")
                continue
                
        # Commit all changes
        session.commit()
        print("Successfully updated fundamental indicators")
        
    except Exception as e:
        session.rollback()
        print(f"Error updating fundamental indicators: {e}")
        
    finally:
        session.close()


def main():
    """
    Main function to update all indicators
    """
    # Symbols to update (in a real application, this might come from a database or config file)
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    print("=== Quantitative Indicator Database Update Script ===")
    print(f"Starting update at {datetime.now()}")
    
    # Update technical indicators
    update_technical_indicators(symbols, days=30)
    
    # Update fundamental indicators
    update_fundamental_indicators(symbols)
    
    print("=== Update Complete ===")


if __name__ == "__main__":
    main()