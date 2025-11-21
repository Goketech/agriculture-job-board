"""
Database module for Local Agricultural Job Board & Skills Matcher

This module handles database initialization, connection management, and query execution.
Owner: Modupe Adegoke Akanni
"""

import sqlite3
import os
from datetime import datetime


# Database configuration
DB_DIR = "data"
DB_NAME = "agri_jobs.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)


def init_database():
    """
    Create database directory and initialize all tables.
    
    Creates the following tables:
    - farmers: Farmer registration and profiles
    - workers: Worker registration and profiles
    - jobs: Job postings
    - matches: Job-worker match results
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create farmers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                email TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create workers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                skills TEXT NOT NULL,
                available BOOLEAN DEFAULT 1,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                skill_required TEXT NOT NULL,
                location TEXT NOT NULL,
                duration TEXT,
                pay_rate TEXT,
                status TEXT DEFAULT 'open',
                posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
            )
        """)
        
        # Create matches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                worker_id INTEGER NOT NULL,
                match_score INTEGER,
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id),
                FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
            )
        """)
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"Database initialized successfully at {DB_PATH}")
        return True
        
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        return False


def get_connection():
    """
    Return a database connection object.
    
    Returns:
        sqlite3.Connection: Database connection object
        
    Raises:
        sqlite3.Error: If connection fails
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise


def execute_query(query, params=None):
    """
    Execute a SQL query safely with parameter binding.
    
    Args:
        query (str): SQL query string
        params (tuple, optional): Parameters for the query
        
    Returns:
        sqlite3.Cursor: Cursor object with executed query
        
    Raises:
        sqlite3.Error: If query execution fails
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        conn.close()
        return cursor
    except sqlite3.Error as e:
        print(f"Query execution error: {e}")
        raise


def fetch_all(query, params=None):
    """
    Fetch all results from a query.
    
    Args:
        query (str): SQL query string
        params (tuple, optional): Parameters for the query
        
    Returns:
        list: List of dictionaries representing rows, or empty list on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Convert rows to dictionaries
        rows = cursor.fetchall()
        conn.close()
        
        # Convert Row objects to dictionaries
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Fetch error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error during fetch: {e}")
        return []


def fetch_one(query, params=None):
    """
    Fetch a single result from a query.
    
    Args:
        query (str): SQL query string
        params (tuple, optional): Parameters for the query
        
    Returns:
        dict: Dictionary representing the row, or None if not found or on error
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        print(f"Fetch error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during fetch: {e}")
        return None


# Database initialization is handled by main.py
# This module should not be run directly

