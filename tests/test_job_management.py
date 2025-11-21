"""
Unit tests for job_management module.

Tests job posting, viewing, searching, and management functions.
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
from models import Job


class TestJobManagement(unittest.TestCase):
    """Test cases for job management operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = os.path.join(self.test_dir, "test_agri_jobs.db")
        database.DB_DIR = self.test_dir
        
        # Initialize test database
        database.init_database()
        
        # Insert test farmer for job posting
        database.execute_query(
            "INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)",
            ("Test Farmer", "1234567890", "Test Location")
        )
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original database path
        database.DB_PATH = self.original_db_path
        database.DB_DIR = "data"
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_post_job_database_insert(self):
        """Test that posting a job inserts data into database."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        job = Job(
            farmer_id=farmer_id,
            title="Test Job",
            description="Test Description",
            skill_required="Planting",
            location="Test Location",
            duration="3 months",
            pay_rate="$500/month",
            status="open"
        )
        
        # Insert into database
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO jobs (farmer_id, title, description, skill_required, 
               location, duration, pay_rate, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (job.farmer_id, job.title, job.description, job.skill_required,
             job.location, job.duration, job.pay_rate, job.status)
        )
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        
        # Verify insertion
        result = database.fetch_one("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Job")
        self.assertEqual(result['skill_required'], "Planting")
        self.assertEqual(result['status'], "open")
    
    def test_view_all_jobs(self):
        """Test viewing all jobs."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        # Insert multiple jobs
        for i in range(3):
            database.execute_query(
                """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
                   VALUES (?, ?, ?, ?, ?)""",
                (farmer_id, f"Job {i}", "Planting", f"Location {i}", "open")
            )
        
        # Fetch all jobs
        jobs = database.fetch_all("SELECT * FROM jobs ORDER BY job_id")
        
        self.assertEqual(len(jobs), 3)
        self.assertEqual(jobs[0]['title'], "Job 0")
        self.assertEqual(jobs[2]['title'], "Job 2")
    
    def test_view_farmer_jobs(self):
        """Test viewing jobs for a specific farmer."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        # Insert jobs for this farmer
        database.execute_query(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (farmer_id, "Farmer Job", "Planting", "Location", "open")
        )
        
        # Fetch farmer's jobs
        jobs = database.fetch_all(
            "SELECT * FROM jobs WHERE farmer_id = ?",
            (farmer_id,)
        )
        
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['title'], "Farmer Job")
    
    def test_search_jobs_by_location(self):
        """Test searching jobs by location."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        # Insert jobs with different locations
        database.execute_query(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (farmer_id, "Kigali Job", "Planting", "Kigali, Rwanda", "open")
        )
        database.execute_query(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (farmer_id, "Other Job", "Harvesting", "Other Location", "open")
        )
        
        # Search for Kigali jobs
        jobs = database.fetch_all(
            "SELECT * FROM jobs WHERE location LIKE ?",
            ("%Kigali%",)
        )
        
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['title'], "Kigali Job")
    
    def test_update_job_status(self):
        """Test updating job status."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        # Insert job
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (farmer_id, "Test Job", "Planting", "Location", "open")
        )
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        
        # Update status
        database.execute_query(
            "UPDATE jobs SET status = ? WHERE job_id = ?",
            ("filled", job_id)
        )
        
        # Verify update
        result = database.fetch_one("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        self.assertEqual(result['status'], "filled")
    
    def test_delete_job(self):
        """Test deleting a job."""
        farmer = database.fetch_one("SELECT farmer_id FROM farmers LIMIT 1")
        farmer_id = farmer['farmer_id']
        
        # Insert job
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO jobs (farmer_id, title, skill_required, location, status) 
               VALUES (?, ?, ?, ?, ?)""",
            (farmer_id, "Test Job", "Planting", "Location", "open")
        )
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        
        # Delete job
        database.execute_query("DELETE FROM jobs WHERE job_id = ?", (job_id,))
        
        # Verify deletion
        result = database.fetch_one("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

