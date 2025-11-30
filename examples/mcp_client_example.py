"""
MCP Client Example
=================

This script demonstrates how to call the MCP service endpoints.
"""

import requests
import json


# Service base URL - adjust according to where your service is hosted
BASE_URL = "http://localhost:5000"


def call_sma_service(prices, period=14):
    """Call SMA calculation service"""
    url = f"{BASE_URL}/tools/technical_indicators/sma"
    payload = {
        "prices": prices,
        "period": period
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def call_rsi_service(prices, period=14):
    """Call RSI calculation service"""
    url = f"{BASE_URL}/tools/technical_indicators/rsi"
    payload = {
        "prices": prices,
        "period": period
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def call_pe_ratio_service(price, eps):
    """Call P/E ratio calculation service"""
    url = f"{BASE_URL}/tools/fundamental_indicators/pe_ratio"
    payload = {
        "price": price,
        "earnings_per_share": eps
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def main():
    """Example usage of the MCP services"""
    print("=== MCP Client Example ===")
    
    # Example data
    sample_prices = [100, 102, 101, 103, 105, 107, 106, 108, 110, 112]
    
    # Test SMA service
    print("\n1. Testing SMA Service:")
    result = call_sma_service(sample_prices, period=5)
    print(f"SMA Result: {result}")
    
    # Test RSI service
    print("\n2. Testing RSI Service:")
    result = call_rsi_service(sample_prices, period=5)
    print(f"RSI Result: {result}")
    
    # Test P/E ratio service
    print("\n3. Testing P/E Ratio Service:")
    result = call_pe_ratio_service(100, 5)
    print(f"P/E Ratio Result: {result}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()