"""
MCP Service Module
=================

This module provides a Model Control Protocol service that can be called by Dify.ai platform.
It exposes quant indicator functions as API endpoints.
"""

import json
from typing import Dict, Any, List
from flask import Flask, request, jsonify
from functools import wraps

from quant_indicator_db.indicators.technical_indicators import sma, ema, macd, macd_sensitive, rsi
from quant_indicator_db.indicators.fundamental_indicators import (
    price_to_earnings, price_to_book, dividend_yield, debt_to_equity, roe, roa
)
from quant_indicator_db.data.fetcher import DataFetcher
from quant_indicator_db.data.processor import DataProcessor


app = Flask(__name__)


def validate_json(f):
    """Decorator to validate JSON input"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return wrapper


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "quant-indicator-mcp-service"})


@app.route('/tools/technical_indicators/sma', methods=['POST'])
@validate_json
def calculate_sma():
    """Calculate Simple Moving Average"""
    try:
        data = request.get_json()
        prices = data.get('prices')
        period = data.get('period', 14)
        
        if not prices:
            return jsonify({"error": "Prices data is required"}), 400
            
        if not isinstance(prices, list):
            return jsonify({"error": "Prices must be a list"}), 400
            
        if period <= 0:
            return jsonify({"error": "Period must be positive"}), 400
            
        result = sma(prices, period).tolist()
        return jsonify({"sma": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/technical_indicators/ema', methods=['POST'])
@validate_json
def calculate_ema():
    """Calculate Exponential Moving Average"""
    try:
        data = request.get_json()
        prices = data.get('prices')
        period = data.get('period', 14)
        
        if not prices:
            return jsonify({"error": "Prices data is required"}), 400
            
        if not isinstance(prices, list):
            return jsonify({"error": "Prices must be a list"}), 400
            
        if period <= 0:
            return jsonify({"error": "Period must be positive"}), 400
            
        result = ema(prices, period).tolist()
        return jsonify({"ema": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/technical_indicators/macd', methods=['POST'])
@validate_json
def calculate_macd():
    """Calculate MACD"""
    try:
        data = request.get_json()
        prices = data.get('prices')
        fast_period = data.get('fast_period', 12)
        slow_period = data.get('slow_period', 26)
        signal_period = data.get('signal_period', 9)
        
        if not prices:
            return jsonify({"error": "Prices data is required"}), 400
            
        if not isinstance(prices, list):
            return jsonify({"error": "Prices must be a list"}), 400
            
        if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
            return jsonify({"error": "Periods must be positive"}), 400
            
        macd_line, signal_line, histogram = macd(prices, fast_period, slow_period, signal_period)
        return jsonify({
            "macd_line": macd_line.tolist(),
            "signal_line": signal_line.tolist(),
            "histogram": histogram.tolist()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/technical_indicators/macd_sensitive', methods=['POST'])
@validate_json
def calculate_macd_sensitive():
    """Calculate Sensitive MACD"""
    try:
        data = request.get_json()
        prices = data.get('prices')
        fast_period = data.get('fast_period', 8)
        slow_period = data.get('slow_period', 17)
        signal_period = data.get('signal_period', 9)
        
        if not prices:
            return jsonify({"error": "Prices data is required"}), 400
            
        if not isinstance(prices, list):
            return jsonify({"error": "Prices must be a list"}), 400
            
        if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
            return jsonify({"error": "Periods must be positive"}), 400
            
        macd_line, signal_line, histogram = macd_sensitive(prices, fast_period, slow_period, signal_period)
        return jsonify({
            "macd_line": macd_line.tolist(),
            "signal_line": signal_line.tolist(),
            "histogram": histogram.tolist()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/technical_indicators/rsi', methods=['POST'])
@validate_json
def calculate_rsi():
    """Calculate RSI"""
    try:
        data = request.get_json()
        prices = data.get('prices')
        period = data.get('period', 14)
        
        if not prices:
            return jsonify({"error": "Prices data is required"}), 400
            
        if not isinstance(prices, list):
            return jsonify({"error": "Prices must be a list"}), 400
            
        if period <= 0:
            return jsonify({"error": "Period must be positive"}), 400
            
        result = rsi(prices, period).tolist()
        return jsonify({"rsi": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/pe_ratio', methods=['POST'])
@validate_json
def calculate_pe_ratio():
    """Calculate Price to Earnings Ratio"""
    try:
        data = request.get_json()
        price = data.get('price')
        eps = data.get('earnings_per_share')
        
        if price is None or eps is None:
            return jsonify({"error": "Both price and earnings_per_share are required"}), 400
            
        result = price_to_earnings(price, eps)
        return jsonify({"pe_ratio": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/pb_ratio', methods=['POST'])
@validate_json
def calculate_pb_ratio():
    """Calculate Price to Book Ratio"""
    try:
        data = request.get_json()
        price = data.get('price')
        bvps = data.get('book_value_per_share')
        
        if price is None or bvps is None:
            return jsonify({"error": "Both price and book_value_per_share are required"}), 400
            
        result = price_to_book(price, bvps)
        return jsonify({"pb_ratio": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/dividend_yield', methods=['POST'])
@validate_json
def calculate_dividend_yield():
    """Calculate Dividend Yield"""
    try:
        data = request.get_json()
        dps = data.get('dividend_per_share')
        price = data.get('price')
        
        if dps is None or price is None:
            return jsonify({"error": "Both dividend_per_share and price are required"}), 400
            
        result = dividend_yield(dps, price)
        return jsonify({"dividend_yield": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/debt_to_equity', methods=['POST'])
@validate_json
def calculate_debt_to_equity():
    """Calculate Debt to Equity Ratio"""
    try:
        data = request.get_json()
        total_debt = data.get('total_debt')
        total_equity = data.get('total_equity')
        
        if total_debt is None or total_equity is None:
            return jsonify({"error": "Both total_debt and total_equity are required"}), 400
            
        result = debt_to_equity(total_debt, total_equity)
        return jsonify({"debt_to_equity": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/roe', methods=['POST'])
@validate_json
def calculate_roe():
    """Calculate Return on Equity"""
    try:
        data = request.get_json()
        net_income = data.get('net_income')
        total_equity = data.get('total_equity')
        
        if net_income is None or total_equity is None:
            return jsonify({"error": "Both net_income and total_equity are required"}), 400
            
        result = roe(net_income, total_equity)
        return jsonify({"roe": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/fundamental_indicators/roa', methods=['POST'])
@validate_json
def calculate_roa():
    """Calculate Return on Assets"""
    try:
        data = request.get_json()
        net_income = data.get('net_income')
        total_assets = data.get('total_assets')
        
        if net_income is None or total_assets is None:
            return jsonify({"error": "Both net_income and total_assets are required"}), 400
            
        result = roa(net_income, total_assets)
        return jsonify({"roa": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/data/fetch_stock_data', methods=['POST'])
@validate_json
def fetch_stock_data():
    """Fetch stock data"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not symbol or not start_date or not end_date:
            return jsonify({"error": "symbol, start_date, and end_date are required"}), 400
            
        fetcher = DataFetcher()
        df = fetcher.fetch_stock_data(symbol, start_date, end_date)
        
        # Convert dataframe to dict for JSON serialization
        result = {
            "dates": df.index.strftime('%Y-%m-%d').tolist(),
            "open": df['open'].tolist(),
            "high": df['high'].tolist(),
            "low": df['low'].tolist(),
            "close": df['close'].tolist(),
            "volume": df['volume'].tolist()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_mcp_service(host='0.0.0.0', port=5000, debug=False):
    """
    Run the MCP service
    
    Args:
        host (str): Host address to bind to
        port (int): Port to listen on
        debug (bool): Enable debug mode
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_mcp_service()