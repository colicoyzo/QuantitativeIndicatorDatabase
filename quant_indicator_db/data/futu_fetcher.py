"""
Futu API Data Fetcher Module
===========================

This module handles fetching financial data from Futu API (富途API).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from futu import *

# Try to import Futu API, but make it optional
try:
    from futu import OpenQuoteContext, TrdEnv, Market, SecurityType
    FUTU_AVAILABLE = True
except ImportError:
    FUTU_AVAILABLE = False
    print("Warning: Futu API not installed. Install with 'pip install futu-api'")


class FutuDataFetcher:
    """
    A class to fetch financial data from Futu API (富途API)
    """
    
    def __init__(self, host='127.0.0.1', port=11111):
        """
        Initialize the FutuDataFetcher
        
        Args:
            host (str): FutuOpenD host address
            port (int): FutuOpenD port
        """
        if not FUTU_AVAILABLE:
            raise ImportError("Futu API is not installed. Please install with 'pip install futu-api'")
            
        self.host = host
        self.port = port
        self.quote_ctx = None
        self.connected = False
    
    def connect(self):
        """
        Connect to Futu OpenD server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.quote_ctx = OpenQuoteContext(host=self.host, port=self.port)
            self.connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to Futu OpenD: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Disconnect from Futu OpenD server
        """
        if self.quote_ctx:
            self.quote_ctx.close()
            self.connected = False
    
    def fetch_historical_data(self, symbol, start_date, end_date, market='HK'):
        """
        Fetch historical stock price data for a given symbol
        
        Args:
            symbol (str): Stock symbol (e.g., '00700' for Tencent)
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            market (str): Market code ('HK', 'US', 'SH', 'SZ')
            
        Returns:
            pd.DataFrame: DataFrame containing OHLCV data
        """
        if not self.connected:
            raise ConnectionError("Not connected to Futu OpenD")
        
        try:
            # Format symbol with market
            if market == 'HK':
                full_symbol = f'HK.{symbol}'
            elif market == 'US':
                full_symbol = f'US.{symbol}'
            elif market in ['SH', 'SZ']:
                full_symbol = f'{market}.{symbol}'
            else:
                full_symbol = symbol
            
            # Get historical K-line data
            ret, data, page_req_key = self.quote_ctx.request_history_kline(
                code=full_symbol,
                start=start_date,
                end=end_date,
                ktype=KLType.K_DAY,  # Daily data
                autype=AuType.QFQ  # Forward adjusted prices
            )
            
            if ret == RET_OK:
                # Convert to our standard format
                df = pd.DataFrame()
                df['date'] = pd.to_datetime(data['time_key'])
                df['open'] = data['open'].astype(float)
                df['high'] = data['high'].astype(float)
                df['low'] = data['low'].astype(float)
                df['close'] = data['close'].astype(float)
                df['volume'] = data['volume'].astype(int)
                
                return df.set_index('date')
            else:
                raise Exception(f"Futu API error: {data}")
                
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            # Return empty DataFrame in case of error
            return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume']).set_index('date')
    
    def fetch_realtime_data(self, symbols, market='HK'):
        """
        Fetch real-time stock data for given symbols
        
        Args:
            symbols (list): List of stock symbols
            market (str): Market code ('HK', 'US', 'SH', 'SZ')
            
        Returns:
            pd.DataFrame: DataFrame containing real-time data
        """
        if not self.connected:
            raise ConnectionError("Not connected to Futu OpenD")
        
        try:
            # Format symbols with market
            full_symbols = []
            for symbol in symbols:
                if market == 'HK':
                    full_symbols.append(f'HK.{symbol}')
                elif market == 'US':
                    full_symbols.append(f'US.{symbol}')
                elif market in ['SH', 'SZ']:
                    full_symbols.append(f'{market}.{symbol}')
                else:
                    full_symbols.append(symbol)
            
            # Get real-time quotes
            ret, data = self.quote_ctx.get_stock_quote(full_symbols)
            
            if ret == RET_OK:
                # Convert to our standard format
                df = pd.DataFrame()
                df['symbol'] = data['code'].str.split('.').str[1]  # Extract symbol without market prefix
                df['last_price'] = data['last_price'].astype(float)
                df['open'] = data['open'].astype(float)
                df['high'] = data['high'].astype(float)
                df['low'] = data['low'].astype(float)
                df['volume'] = data['volume'].astype(int)
                df['turnover'] = data['turnover'].astype(float)
                df['timestamp'] = pd.to_datetime(data['update_time'])
                
                return df.set_index('symbol')
            else:
                raise Exception(f"Futu API error: {data}")
                
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            # Return empty DataFrame in case of error
            return pd.DataFrame(columns=['symbol', 'last_price', 'open', 'high', 'low', 'volume', 'turnover', 'timestamp']).set_index('symbol')
    
    def fetch_fundamental_data(self, symbol, market='HK'):
        """
        Fetch basic fundamental data for a given symbol
        
        Args:
            symbol (str): Stock symbol
            market (str): Market code ('HK', 'US', 'SH', 'SZ')
            
        Returns:
            dict: Dictionary containing fundamental data
        """
        if not self.connected:
            raise ConnectionError("Not connected to Futu OpenD")
        
        try:
            # Format symbol with market
            if market == 'HK':
                full_symbol = f'HK.{symbol}'
            elif market == 'US':
                full_symbol = f'US.{symbol}'
            elif market in ['SH', 'SZ']:
                full_symbol = f'{market}.{symbol}'
            else:
                full_symbol = symbol
            
            # Get snapshot data
            ret, data = self.quote_ctx.get_market_snapshot([full_symbol])
            
            if ret == RET_OK and not data.empty:
                # Extract fundamental data
                row = data.iloc[0]
                return {
                    'symbol': symbol,
                    'pe_ratio': float(row['pe_ratio']) if row['pe_ratio'] != '--' else None,
                    'pb_ratio': float(row['pb_ratio']) if row['pb_ratio'] != '--' else None,
                    'dividend_yield': float(row['dividend_yield']) if row['dividend_yield'] != '--' else None,
                    'market_cap': float(row['market_val']) if row['market_val'] != '--' else None,
                    'total_equity': None,  # Not directly available in snapshot
                    'net_income': None,    # Not directly available in snapshot
                    'total_assets': None,  # Not directly available in snapshot
                    'timestamp': datetime.now()
                }
            else:
                raise Exception(f"Futu API error: {data if 'data' in locals() else 'No data returned'}")
                
        except Exception as e:
            print(f"Error fetching fundamental data: {e}")
            # Return empty dict in case of error
            return {}