"""
Tests for fundamental indicators module
"""

import pytest
import numpy as np
from quant_indicator_db.indicators.fundamental_indicators import (
    price_to_earnings, price_to_book, dividend_yield, debt_to_equity, roe, roa
)


def test_price_to_earnings():
    """Test P/E ratio calculation"""
    pe = price_to_earnings(100, 5)
    assert pe == 20.0


def test_price_to_earnings_zero_eps():
    """Test P/E ratio with zero EPS"""
    with pytest.raises(ValueError):
        price_to_earnings(100, 0)


def test_price_to_book():
    """Test P/B ratio calculation"""
    pb = price_to_book(100, 20)
    assert pb == 5.0


def test_price_to_book_zero_bv():
    """Test P/B ratio with zero book value"""
    with pytest.raises(ValueError):
        price_to_book(100, 0)


def test_dividend_yield():
    """Test dividend yield calculation"""
    dy = dividend_yield(5, 100)
    assert dy == 0.05


def test_dividend_yield_zero_price():
    """Test dividend yield with zero price"""
    with pytest.raises(ValueError):
        dividend_yield(5, 0)


def test_debt_to_equity():
    """Test debt to equity ratio calculation"""
    de = debt_to_equity(1000, 2000)
    assert de == 0.5


def test_debt_to_equity_zero_equity():
    """Test debt to equity ratio with zero equity"""
    with pytest.raises(ValueError):
        debt_to_equity(1000, 0)


def test_roe():
    """Test Return on Equity calculation"""
    roe_value = roe(100, 1000)
    assert roe_value == 0.1


def test_roe_zero_equity():
    """Test ROE with zero equity"""
    with pytest.raises(ValueError):
        roe(100, 0)


def test_roa():
    """Test Return on Assets calculation"""
    roa_value = roa(100, 2000)
    assert roa_value == 0.05


def test_roa_zero_assets():
    """Test ROA with zero assets"""
    with pytest.raises(ValueError):
        roa(100, 0)