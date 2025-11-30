"""
Sync Futu Data Script
====================

This script fetches data from Futu API and stores it in the database.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quant_indicator_db.data.futu_fetcher import FutuDataFetcher
from quant_indicator_db.database.connector import get_connector
from quant_indicator_db.database.models import StockData, FundamentalData


def sync_historical_data(symbols, days=30, market='HK'):
    """
    Sync historical data from Futu API to database
    
    Args:
        symbols (list): List of stock symbols
        days (int): Number of days of historical data to sync
        market (str): Market code ('HK', 'US', 'SH', 'SZ')
    """
    print(f"Syncing historical data for {len(symbols)} symbols...")
    
    # Initialize components
    try:
        fetcher = FutuDataFetcher()
        if not fetcher.connect():
            print("Failed to connect to Futu API")
            return
    except ImportError:
        print("Futu API not installed. Skipping historical data sync.")
        return
    
    db_connector = get_connector()
    session = db_connector.get_session()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        for symbol in symbols:
            print(f"Processing historical data for {symbol}...")
            
            # Fetch data from Futu API
            try:
                data = fetcher.fetch_historical_data(
                    symbol, 
                    start_date.strftime('%Y-%m-%d'), 
                    end_date.strftime('%Y-%m-%d'),
                    market
                )
                
                if data.empty:
                    print(f"No historical data for {symbol}")
                    continue
                
                # Save to database
                for index, row in data.iterrows():
                    stock_data = StockData(
                        symbol=symbol,
                        date=index,
                        open_price=float(row['open']),
                        high_price=float(row['high']),
                        low_price=float(row['low']),
                        close_price=float(row['close']),
                        volume=int(row['volume'])
                    )
                    session.merge(stock_data)  # Use merge to handle duplicates
                
                session.commit()
                print(f"Saved {len(data)} records for {symbol}")
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                session.rollback()
                continue
        
        print("Historical data sync completed!")
        
    except Exception as e:
        print(f"Error syncing historical data: {e}")
        session.rollback()
        
    finally:
        session.close()
        fetcher.disconnect()


def sync_realtime_data(symbols, market='HK'):
    """
    Sync real-time data from Futu API to database
    
    Args:
        symbols (list): List of stock symbols
        market (str): Market code ('HK', 'US', 'SH', 'SZ')
    """
    print(f"Syncing real-time data for {len(symbols)} symbols...")
    
    # Initialize components
    try:
        fetcher = FutuDataFetcher()
        if not fetcher.connect():
            print("Failed to connect to Futu API")
            return
    except ImportError:
        print("Futu API not installed. Skipping real-time data sync.")
        return
    
    db_connector = get_connector()
    session = db_connector.get_session()
    
    try:
        # Fetch data from Futu API
        data = fetcher.fetch_realtime_data(symbols, market)
        
        if data.empty:
            print("No real-time data fetched")
            return
        
        # Save to database
        for symbol, row in data.iterrows():
            stock_data = StockData(
                symbol=symbol,
                date=row['timestamp'],
                open_price=float(row['open']),
                high_price=float(row['high']),
                low_price=float(row['low']),
                close_price=float(row['last_price']),
                volume=int(row['volume'])
            )
            session.merge(stock_data)  # Use merge to handle duplicates
        
        session.commit()
        print(f"Saved real-time data for {len(data)} symbols")
        print("Real-time data sync completed!")
        
    except Exception as e:
        print(f"Error syncing real-time data: {e}")
        session.rollback()
        
    finally:
        session.close()
        fetcher.disconnect()


def sync_fundamental_data(symbols, market='HK'):
    """
    Sync fundamental data from Futu API to database
    
    Args:
        symbols (list): List of stock symbols
        market (str): Market code ('HK', 'US', 'SH', 'SZ')
    """
    print(f"Syncing fundamental data for {len(symbols)} symbols...")
    
    # Initialize components
    try:
        fetcher = FutuDataFetcher()
        if not fetcher.connect():
            print("Failed to connect to Futu API")
            return
    except ImportError:
        print("Futu API not installed. Skipping fundamental data sync.")
        return
    
    db_connector = get_connector()
    session = db_connector.get_session()
    
    try:
        for symbol in symbols:
            print(f"Processing fundamental data for {symbol}...")
            
            # Fetch data from Futu API
            try:
                data = fetcher.fetch_fundamental_data(symbol, market)
                
                if not data:
                    print(f"No fundamental data for {symbol}")
                    continue
                
                # Save to database
                fundamental_data = FundamentalData(
                    symbol=data['symbol'],
                    pe_ratio=data.get('pe_ratio'),
                    pb_ratio=data.get('pb_ratio'),
                    dividend_yield=data.get('dividend_yield'),
                    market_cap=data.get('market_cap'),
                    total_debt=data.get('total_debt'),
                    total_equity=data.get('total_equity'),
                    net_income=data.get('net_income'),
                    total_assets=data.get('total_assets'),
                    timestamp=data.get('timestamp', datetime.now())
                )
                session.merge(fundamental_data)  # Use merge to handle duplicates
                
                session.commit()
                print(f"Saved fundamental data for {symbol}")
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                session.rollback()
                continue
        
        print("Fundamental data sync completed!")
        
    except Exception as e:
        print(f"Error syncing fundamental data: {e}")
        session.rollback()
        
    finally:
        session.close()
        fetcher.disconnect()


def main():
    """
    Main function to sync data from Futu API
    """
    # Symbols to sync (in a real application, this might come from a database or config file)
    symbols = ['00700', '00001', '00002']  # Example HK stock codes
    
    print("=== Quantitative Indicator Database - Futu Data Sync ===")
    print(f"Starting sync at {datetime.now()}")
    
    # Sync historical data (last 30 days)
    sync_historical_data(symbols, days=30, market='HK')
    
    # Sync real-time data
    sync_realtime_data(symbols, market='HK')
    
    # Sync fundamental data
    sync_fundamental_data(symbols, market='HK')
    
    print("=== Data Sync Complete ===")


if __name__ == "__main__":
    main()