import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import os
import sqlite3
from database import init_database, get_connection, execute_query, fetch_one, fetch_all

DB_PATH = "data/agri_jobs.db"

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database
        init_database()

    def test_tables_created(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Check if tables exist
        tables = ['farmers', 'workers', 'jobs', 'matches']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
            self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_insert_and_fetch_farmer(self):
        execute_query("INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)", 
                      ("Test Farmer", "1234567890", "Testville"))
        farmer = fetch_one("SELECT * FROM farmers WHERE name=?", ("Test Farmer",))
        self.assertIsNotNone(farmer)
        self.assertEqual(farmer["name"], "Test Farmer")  

    def test_insert_and_fetch_worker(self):
        execute_query("INSERT INTO workers (name, phone, location, skills) VALUES (?, ?, ?, ?)",
                      ("Test Worker", "0987654321", "Testville", "planting"))
        worker = fetch_one("SELECT * FROM workers WHERE name=?", ("Test Worker",))
        self.assertIsNotNone(worker)
        self.assertEqual(worker["name"], "Test Worker")

if __name__ == "__main__":
    unittest.main()
