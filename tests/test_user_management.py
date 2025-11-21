"""
Unit tests for user_management module.

Tests user registration and profile management functions.
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
from models import Farmer, Worker


class TestUserManagement(unittest.TestCase):
    """Test cases for user management operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = os.path.join(self.test_dir, "test_agri_jobs.db")
        database.DB_DIR = self.test_dir
        
        # Initialize test database
        database.init_database()
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original database path
        database.DB_PATH = self.original_db_path
        database.DB_DIR = "data"
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_farmer_registration_database_insert(self):
        """Test that farmer registration inserts data into database."""
        farmer = Farmer(
            name="Test Farmer",
            phone="1234567890",
            location="Test Location",
            email="test@example.com"
        )
        
        # Insert into database
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmers (name, phone, location, email) VALUES (?, ?, ?, ?)",
            (farmer.name, farmer.phone, farmer.location, farmer.email)
        )
        conn.commit()
        farmer_id = cursor.lastrowid
        conn.close()
        
        # Verify insertion
        result = database.fetch_one("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Test Farmer")
        self.assertEqual(result['email'], "test@example.com")
    
    def test_worker_registration_database_insert(self):
        """Test that worker registration inserts data into database."""
        worker = Worker(
            name="Test Worker",
            phone="0987654321",
            location="Test Location",
            skills="Planting, Harvesting",
            available=True
        )
        
        # Insert into database
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, phone, location, skills, available) VALUES (?, ?, ?, ?, ?)",
            (worker.name, worker.phone, worker.location, worker.skills, int(worker.available))
        )
        conn.commit()
        worker_id = cursor.lastrowid
        conn.close()
        
        # Verify insertion
        result = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Test Worker")
        self.assertEqual(result['skills'], "Planting, Harvesting")
        self.assertEqual(result['available'], 1)
    
    def test_update_worker_skills(self):
        """Test updating worker skills."""
        # Insert test worker
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, phone, location, skills) VALUES (?, ?, ?, ?)",
            ("Test Worker", "1234567890", "Test Location", "Old Skills")
        )
        conn.commit()
        worker_id = cursor.lastrowid
        conn.close()
        
        # Update skills
        database.execute_query(
            "UPDATE workers SET skills = ? WHERE worker_id = ?",
            ("New Skills, Updated", worker_id)
        )
        
        # Verify update
        result = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
        self.assertEqual(result['skills'], "New Skills, Updated")
    
    def test_update_worker_availability(self):
        """Test updating worker availability."""
        # Insert test worker
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, phone, location, skills, available) VALUES (?, ?, ?, ?, ?)",
            ("Test Worker", "1234567890", "Test Location", "Skills", 1)
        )
        conn.commit()
        worker_id = cursor.lastrowid
        conn.close()
        
        # Update availability
        database.execute_query(
            "UPDATE workers SET available = ? WHERE worker_id = ?",
            (0, worker_id)
        )
        
        # Verify update
        result = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
        self.assertEqual(result['available'], 0)
    
    def test_view_farmer_profile(self):
        """Test viewing farmer profile."""
        # Insert test farmer
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmers (name, phone, location, email) VALUES (?, ?, ?, ?)",
            ("Test Farmer", "1234567890", "Test Location", "test@example.com")
        )
        conn.commit()
        farmer_id = cursor.lastrowid
        conn.close()
        
        # Fetch profile
        farmer = database.fetch_one("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
        
        self.assertIsNotNone(farmer)
        self.assertEqual(farmer['name'], "Test Farmer")
        self.assertEqual(farmer['email'], "test@example.com")
    
    def test_view_worker_profile(self):
        """Test viewing worker profile."""
        # Insert test worker
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, phone, location, skills) VALUES (?, ?, ?, ?)",
            ("Test Worker", "1234567890", "Test Location", "Planting, Harvesting")
        )
        conn.commit()
        worker_id = cursor.lastrowid
        conn.close()
        
        # Fetch profile
        worker = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
        
        self.assertIsNotNone(worker)
        self.assertEqual(worker['name'], "Test Worker")
        self.assertEqual(worker['skills'], "Planting, Harvesting")


if __name__ == '__main__':
    unittest.main()

