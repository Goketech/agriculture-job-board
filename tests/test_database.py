"""
Unit tests for database module.

Tests database initialization, connection management, and query execution.
"""

import unittest
import os
import sqlite3
import tempfile
import shutil
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database


class TestDatabase(unittest.TestCase):
    """Test cases for database operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = os.path.join(self.test_dir, "test_agri_jobs.db")
        database.DB_DIR = self.test_dir
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original database path
        database.DB_PATH = self.original_db_path
        database.DB_DIR = "data"
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init_database_creates_directory(self):
        """Test that init_database creates the data directory if it doesn't exist."""
        # Remove test directory if it exists
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        result = database.init_database()
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(database.DB_PATH))
    
    def test_init_database_creates_tables(self):
        """Test that init_database creates all required tables."""
        database.init_database()
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Check that all tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('farmers', 'workers', 'jobs', 'matches')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.assertIn('farmers', tables)
        self.assertIn('workers', tables)
        self.assertIn('jobs', tables)
        self.assertIn('matches', tables)
    
    def test_get_connection(self):
        """Test that get_connection returns a valid connection."""
        database.init_database()
        conn = database.get_connection()
        
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_get_connection_row_factory(self):
        """Test that connection uses Row factory for column access by name."""
        database.init_database()
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute("""
            INSERT INTO farmers (name, phone, location, email)
            VALUES (?, ?, ?, ?)
        """, ("Test Farmer", "1234567890", "Test Location", "test@example.com"))
        conn.commit()
        
        # Fetch using row factory
        cursor.execute("SELECT * FROM farmers WHERE name = ?", ("Test Farmer",))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], "Test Farmer")
        self.assertEqual(row['phone'], "1234567890")
    
    def test_execute_query(self):
        """Test execute_query function."""
        database.init_database()
        
        database.execute_query("""
            INSERT INTO farmers (name, phone, location)
            VALUES (?, ?, ?)
        """, ("Test Farmer", "1234567890", "Test Location"))
        
        # Verify insertion
        result = database.fetch_one(
            "SELECT * FROM farmers WHERE name = ?",
            ("Test Farmer",)
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Test Farmer")
    
    def test_fetch_all(self):
        """Test fetch_all function."""
        database.init_database()
        
        # Insert multiple records
        for i in range(3):
            database.execute_query("""
                INSERT INTO farmers (name, phone, location)
                VALUES (?, ?, ?)
            """, (f"Farmer {i}", f"123456789{i}", f"Location {i}"))
        
        # Fetch all
        results = database.fetch_all("SELECT * FROM farmers ORDER BY name")
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['name'], "Farmer 0")
        self.assertEqual(results[2]['name'], "Farmer 2")
    
    def test_fetch_one(self):
        """Test fetch_one function."""
        database.init_database()
        
        database.execute_query("""
            INSERT INTO farmers (name, phone, location)
            VALUES (?, ?, ?)
        """, ("Test Farmer", "1234567890", "Test Location"))
        
        result = database.fetch_one(
            "SELECT * FROM farmers WHERE name = ?",
            ("Test Farmer",)
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Test Farmer")
        
        # Test non-existent record
        result = database.fetch_one(
            "SELECT * FROM farmers WHERE name = ?",
            ("Non-existent",)
        )
        self.assertIsNone(result)
    
    def test_fetch_all_returns_list_of_dicts(self):
        """Test that fetch_all returns list of dictionaries."""
        database.init_database()
        
        database.execute_query("""
            INSERT INTO farmers (name, phone, location)
            VALUES (?, ?, ?)
        """, ("Test Farmer", "1234567890", "Test Location"))
        
        results = database.fetch_all("SELECT * FROM farmers")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], dict)
        self.assertIn('name', results[0])
        self.assertIn('phone', results[0])


if __name__ == '__main__':
    unittest.main()

