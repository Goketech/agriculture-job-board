"""
Unit tests for models module.

Tests data validation functions and model classes.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    validate_phone,
    validate_email,
    validate_location,
    Farmer,
    Worker,
    Job
)


class TestValidationFunctions(unittest.TestCase):
    """Test cases for validation functions."""
    
    def test_validate_phone_valid_formats(self):
        """Test phone validation with various valid formats."""
        valid_phones = [
            "1234567890",
            "123-456-7890",
            "123 456 7890",
            "(123) 456-7890",
            "+1234567890",
            "+1-234-567-8900"
        ]
        
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(validate_phone(phone), f"Should accept: {phone}")
    
    def test_validate_phone_invalid_formats(self):
        """Test phone validation with invalid formats."""
        invalid_phones = [
            "",
            "123",  # Too short
            "1234567890123456",  # Too long
            "abc1234567",  # Contains letters
            "123-456",  # Too short
            None
        ]
        
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertFalse(validate_phone(phone), f"Should reject: {phone}")
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "test123@test-domain.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should accept: {email}")
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            "",
            "notanemail",
            "@example.com",
            "user@",
            "user@domain",
            "user space@example.com",
            None
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should reject: {email}")
    
    def test_validate_location_valid(self):
        """Test location validation with valid locations."""
        valid_locations = [
            "Kigali, Rwanda",
            "New York",
            "123 Main Street",
            "A" * 100  # Reasonable length
        ]
        
        for location in valid_locations:
            with self.subTest(location=location):
                self.assertTrue(validate_location(location), f"Should accept: {location}")
    
    def test_validate_location_invalid(self):
        """Test location validation with invalid locations."""
        invalid_locations = [
            "",
            " ",
            "A" * 201,  # Too long
            None
        ]
        
        for location in invalid_locations:
            with self.subTest(location=location):
                self.assertFalse(validate_location(location), f"Should reject: {location}")


class TestFarmerModel(unittest.TestCase):
    """Test cases for Farmer model."""
    
    def test_farmer_creation(self):
        """Test creating a Farmer instance."""
        farmer = Farmer(
            name="John Doe",
            phone="1234567890",
            location="Kigali, Rwanda",
            email="john@example.com"
        )
        
        self.assertEqual(farmer.name, "John Doe")
        self.assertEqual(farmer.phone, "1234567890")
        self.assertEqual(farmer.location, "Kigali, Rwanda")
        self.assertEqual(farmer.email, "john@example.com")
    
    def test_farmer_validation_valid(self):
        """Test farmer validation with valid data."""
        farmer = Farmer(
            name="John Doe",
            phone="1234567890",
            location="Kigali, Rwanda",
            email="john@example.com"
        )
        
        is_valid, error = farmer.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_farmer_validation_missing_name(self):
        """Test farmer validation with missing name."""
        farmer = Farmer(
            name="",
            phone="1234567890",
            location="Kigali, Rwanda"
        )
        
        is_valid, error = farmer.validate()
        self.assertFalse(is_valid)
        self.assertIn("Name", error)
    
    def test_farmer_validation_invalid_phone(self):
        """Test farmer validation with invalid phone."""
        farmer = Farmer(
            name="John Doe",
            phone="123",  # Too short
            location="Kigali, Rwanda"
        )
        
        is_valid, error = farmer.validate()
        self.assertFalse(is_valid)
        self.assertIn("phone", error.lower())
    
    def test_farmer_validation_invalid_email(self):
        """Test farmer validation with invalid email."""
        farmer = Farmer(
            name="John Doe",
            phone="1234567890",
            location="Kigali, Rwanda",
            email="notanemail"
        )
        
        is_valid, error = farmer.validate()
        self.assertFalse(is_valid)
        self.assertIn("email", error.lower())
    
    def test_farmer_to_dict(self):
        """Test farmer to_dict method."""
        farmer = Farmer(
            name="John Doe",
            phone="1234567890",
            location="Kigali, Rwanda",
            email="john@example.com",
            farmer_id=1
        )
        
        farmer_dict = farmer.to_dict()
        
        self.assertIsInstance(farmer_dict, dict)
        self.assertEqual(farmer_dict['name'], "John Doe")
        self.assertEqual(farmer_dict['farmer_id'], 1)


class TestWorkerModel(unittest.TestCase):
    """Test cases for Worker model."""
    
    def test_worker_creation(self):
        """Test creating a Worker instance."""
        worker = Worker(
            name="Jane Smith",
            phone="0987654321",
            location="Kigali, Rwanda",
            skills="Planting, Harvesting, Irrigation",
            available=True
        )
        
        self.assertEqual(worker.name, "Jane Smith")
        self.assertEqual(worker.skills, "Planting, Harvesting, Irrigation")
        self.assertTrue(worker.available)
    
    def test_worker_validation_valid(self):
        """Test worker validation with valid data."""
        worker = Worker(
            name="Jane Smith",
            phone="0987654321",
            location="Kigali, Rwanda",
            skills="Planting, Harvesting"
        )
        
        is_valid, error = worker.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_worker_validation_missing_skills(self):
        """Test worker validation with missing skills."""
        worker = Worker(
            name="Jane Smith",
            phone="0987654321",
            location="Kigali, Rwanda",
            skills=""
        )
        
        is_valid, error = worker.validate()
        self.assertFalse(is_valid)
        self.assertIn("skill", error.lower())
    
    def test_worker_get_skills_list(self):
        """Test worker get_skills_list method."""
        worker = Worker(
            name="Jane Smith",
            phone="0987654321",
            location="Kigali, Rwanda",
            skills="Planting, Harvesting, Irrigation"
        )
        
        skills_list = worker.get_skills_list()
        
        self.assertIsInstance(skills_list, list)
        self.assertEqual(len(skills_list), 3)
        self.assertIn("Planting", skills_list)
        self.assertIn("Harvesting", skills_list)
    
    def test_worker_has_skill(self):
        """Test worker has_skill method."""
        worker = Worker(
            name="Jane Smith",
            phone="0987654321",
            location="Kigali, Rwanda",
            skills="Planting, Harvesting"
        )
        
        self.assertTrue(worker.has_skill("Planting"))
        self.assertTrue(worker.has_skill("planting"))  # Case insensitive
        self.assertFalse(worker.has_skill("Irrigation"))


class TestJobModel(unittest.TestCase):
    """Test cases for Job model."""
    
    def test_job_creation(self):
        """Test creating a Job instance."""
        job = Job(
            farmer_id=1,
            title="Farm Worker Needed",
            skill_required="Planting",
            location="Kigali, Rwanda",
            description="Need experienced farm worker",
            duration="3 months",
            pay_rate="$500/month"
        )
        
        self.assertEqual(job.title, "Farm Worker Needed")
        self.assertEqual(job.farmer_id, 1)
        self.assertEqual(job.status, "open")  # Default status
    
    def test_job_validation_valid(self):
        """Test job validation with valid data."""
        job = Job(
            farmer_id=1,
            title="Farm Worker Needed",
            skill_required="Planting",
            location="Kigali, Rwanda"
        )
        
        is_valid, error = job.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_job_validation_missing_title(self):
        """Test job validation with missing title."""
        job = Job(
            farmer_id=1,
            title="",
            skill_required="Planting",
            location="Kigali, Rwanda"
        )
        
        is_valid, error = job.validate()
        self.assertFalse(is_valid)
        self.assertIn("title", error.lower())
    
    def test_job_validation_invalid_status(self):
        """Test job validation with invalid status."""
        job = Job(
            farmer_id=1,
            title="Farm Worker",
            skill_required="Planting",
            location="Kigali, Rwanda",
            status="invalid"
        )
        
        is_valid, error = job.validate()
        self.assertFalse(is_valid)
        self.assertIn("status", error.lower())
    
    def test_job_to_dict(self):
        """Test job to_dict method."""
        job = Job(
            farmer_id=1,
            title="Farm Worker",
            skill_required="Planting",
            location="Kigali, Rwanda",
            job_id=5
        )
        
        job_dict = job.to_dict()
        
        self.assertIsInstance(job_dict, dict)
        self.assertEqual(job_dict['job_id'], 5)
        self.assertEqual(job_dict['title'], "Farm Worker")


if __name__ == '__main__':
    unittest.main()

