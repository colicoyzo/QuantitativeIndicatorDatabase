"""
Start MCP Service Script
========================

This script starts the MCP service for the quant indicator database.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quant_indicator_db.mcp_service import run_mcp_service


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Quant Indicator MCP Service")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print(f"Starting Quant Indicator MCP Service on {args.host}:{args.port}")
    if args.debug:
        print("Debug mode enabled")
        
    run_mcp_service(host=args.host, port=args.port, debug=args.debug)