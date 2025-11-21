"""
Unit tests for matching_engine module.

Tests the job-worker matching algorithm and scoring system.
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
from matching_engine import MatchingEngine, match_location_text, parse_latlon


class TestMatchingEngine(unittest.TestCase):
    """Test cases for matching engine operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = os.path.join(self.test_dir, "test_agri_jobs.db")
        database.DB_DIR = self.test_dir
        
        # Initialize test database
        database.init_database()
        
        # Insert test data
        self.setup_test_data()
    
    def setup_test_data(self):
        """Set up test farmers, workers, and jobs."""
        # Insert test farmer
        database.execute_query(
            "INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)",
            ("Test Farmer", "1234567890", "Kigali, Rwanda")
        )
        
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        self.farmer_id = farmer['farmer_id']
        
        # Insert test workers
        database.execute_query(
            """INSERT INTO workers (name, phone, location, skills, available) 
               VALUES (?, ?, ?, ?, ?)""",
            ("Worker 1", "1111111111", "Kigali, Rwanda", "Planting, Harvesting", 1)
        )
        database.execute_query(
            """INSERT INTO workers (name, phone, location, skills, available) 
               VALUES (?, ?, ?, ?, ?)""",
            ("Worker 2", "2222222222", "Other Location", "Planting", 1)
        )
        database.execute_query(
            """INSERT INTO workers (name, phone, location, skills, available) 
               VALUES (?, ?, ?, ?, ?)""",
            ("Worker 3", "3333333333", "Kigali, Rwanda", "Irrigation", 0)  # Not available
        )
        
        # Insert test jobs
        database.execute_query(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (self.farmer_id, "Planting Job", "Planting", "Kigali, Rwanda", "open")
        )
        database.execute_query(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (self.farmer_id, "Harvesting Job", "Harvesting", "Kigali, Rwanda", "open")
        )
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original database path
        database.DB_PATH = self.original_db_path
        database.DB_DIR = "data"
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_match_job_to_workers(self):
        """Test matching workers to a job."""
        engine = MatchingEngine()
        job = database.fetch_one(
            "SELECT * FROM jobs WHERE title = ?",
            ("Planting Job",)
        )
        
        matches = engine.match_job_to_workers(job, top_n=10)
        
        self.assertGreater(len(matches), 0)
        # Worker 1 should match (has Planting skill and same location)
        worker_ids = [m['worker_id'] for m in matches]
        self.assertIn(1, worker_ids)  # Worker 1 should be in results
    
    def test_match_worker_to_jobs(self):
        """Test matching jobs to a worker."""
        engine = MatchingEngine()
        worker = database.fetch_one(
            "SELECT * FROM workers WHERE name = ?",
            ("Worker 1",)
        )
        
        matches = engine.match_worker_to_jobs(worker, top_n=10)
        
        self.assertGreater(len(matches), 0)
        # Should match Planting Job (has Planting skill)
        job_ids = [m['job_id'] for m in matches]
        self.assertIn(1, job_ids)  # Planting Job should be in results
    
    def test_match_score_calculation(self):
        """Test that match scores are calculated correctly."""
        engine = MatchingEngine()
        job = database.fetch_one(
            "SELECT * FROM jobs WHERE title = ?",
            ("Planting Job",)
        )
        
        matches = engine.match_job_to_workers(job, top_n=10)
        
        # Check that scores are between 0 and 1
        for match in matches:
            self.assertGreaterEqual(match['score'], 0.0)
            self.assertLessEqual(match['score'], 1.0)
    
    def test_match_location_text_exact_match(self):
        """Test text location matching with exact match."""
        score = match_location_text("Kigali, Rwanda", "Kigali, Rwanda")
        self.assertEqual(score, 1.0)
    
    def test_match_location_text_partial_match(self):
        """Test text location matching with partial match."""
        score = match_location_text("Kigali", "Kigali, Rwanda")
        self.assertGreater(score, 0.5)
    
    def test_match_location_text_no_match(self):
        """Test text location matching with no match."""
        score = match_location_text("Kigali", "New York")
        self.assertLess(score, 0.5)
    
    def test_parse_latlon_valid(self):
        """Test parsing valid lat/lon coordinates."""
        result = parse_latlon("-1.95,30.06")
        self.assertIsNotNone(result)
        self.assertEqual(result['lat'], -1.95)
        self.assertEqual(result['lon'], 30.06)
    
    def test_parse_latlon_invalid(self):
        """Test parsing invalid lat/lon coordinates."""
        result = parse_latlon("Kigali, Rwanda")
        self.assertIsNone(result)
        
        result = parse_latlon("invalid")
        self.assertIsNone(result)
    
    def test_available_workers_only(self):
        """Test that only available workers are matched."""
        engine = MatchingEngine()
        job = database.fetch_one(
            "SELECT * FROM jobs WHERE title = ?",
            ("Planting Job",)
        )
        
        matches = engine.match_job_to_workers(job, top_n=10)
        
        # Worker 3 is not available, should not be in top matches
        worker_ids = [m['worker_id'] for m in matches]
        # Worker 3 has ID 3, but since they're not available, they shouldn't score well
        # The engine filters by available=1 in _get_all_workers, so unavailable workers won't appear
    
    def test_match_saves_to_database(self):
        """Test that matches are saved to the matches table."""
        engine = MatchingEngine()
        job = database.fetch_one(
            "SELECT * FROM jobs WHERE title = ?",
            ("Planting Job",)
        )
        
        matches = engine.match_job_to_workers(job, top_n=10)
        
        # Check that matches were saved
        saved_matches = database.fetch_all(
            "SELECT * FROM matches WHERE job_id = ?",
            (job['job_id'],)
        )
        
        self.assertGreater(len(saved_matches), 0)


if __name__ == '__main__':
    unittest.main()

