"""
Database Connector Module
========================

This module manages database connections and provides interfaces for data access.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import sqlite3
import os


class DatabaseConnector:
    """
    A class to manage database connections
    """
    
    def __init__(self, db_url='sqlite:///quant_indicator.db'):
        """
        Initialize the DatabaseConnector
        
        Args:
            db_url (str): Database connection URL
        """
        self.db_url = db_url
        self.engine = None
        self.Session = None
        self.connect()
    
    def connect(self):
        """
        Establish database connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.engine = create_engine(self.db_url)
            self.Session = sessionmaker(bind=self.engine)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            return False
    
    def get_session(self):
        """
        Get a database session
        
        Returns:
            Session: Database session object
        """
        if self.Session is None:
            raise ConnectionError("Database not connected")
        return self.Session()
    
    def close(self):
        """
        Close database connection
        """
        if self.engine:
            self.engine.dispose()
    
    def initialize_database(self):
        """
        Initialize database tables
        """
        from .models import Base
        try:
            Base.metadata.create_all(self.engine)
            return True
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            return False


def get_connector():
    """
    Get a database connector instance
    
    Returns:
        DatabaseConnector: Database connector instance
    """
    return DatabaseConnector()