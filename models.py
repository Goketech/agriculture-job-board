"""
Data models and validation module for Local Agricultural Job Board & Skills Matcher

This module provides data validation functions and model classes for the application.
Owner: Modupe Adegoke Akanni
"""

import re
from datetime import datetime


def validate_phone(phone):
    """
    Validate phone number format.
    
    Accepts formats:
    - 10 digits (e.g., "1234567890")
    - With dashes (e.g., "123-456-7890")
    - With spaces (e.g., "123 456 7890")
    - With parentheses (e.g., "(123) 456-7890")
    - International format with + (e.g., "+1234567890")
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if remaining characters are all digits
    if not cleaned.isdigit():
        return False
    
    # Check length (minimum 10 digits, maximum 15 for international)
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False
    
    return True


def validate_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email.strip()))


def validate_location(location):
    """
    Validate location input.
    
    Location should be non-empty string with reasonable length.
    
    Args:
        location (str): Location to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not location or not isinstance(location, str):
        return False
    
    # Trim whitespace
    location = location.strip()
    
    # Check if not empty and reasonable length
    if len(location) == 0 or len(location) > 200:
        return False
    
    return True


class Farmer:
    """
    Farmer data model class.
    
    Represents a farmer who can post jobs.
    """
    
    def __init__(self, name, phone, location, email=None, farmer_id=None, registration_date=None):
        """
        Initialize Farmer instance.
        
        Args:
            name (str): Farmer's full name
            phone (str): Phone number
            location (str): Location/address
            email (str, optional): Email address
            farmer_id (int, optional): Database ID
            registration_date (str, optional): Registration timestamp
        """
        self.farmer_id = farmer_id
        self.name = name
        self.phone = phone
        self.location = location
        self.email = email
        self.registration_date = registration_date
    
    def validate(self):
        """
        Validate farmer data.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.name or len(self.name.strip()) == 0:
            return False, "Name is required"
        
        if not validate_phone(self.phone):
            return False, "Invalid phone number format"
        
        if not validate_location(self.location):
            return False, "Invalid location"
        
        if self.email and not validate_email(self.email):
            return False, "Invalid email format"
        
        return True, None
    
    def to_dict(self):
        """
        Convert farmer instance to dictionary.
        
        Returns:
            dict: Dictionary representation of farmer
        """
        return {
            'farmer_id': self.farmer_id,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'email': self.email,
            'registration_date': self.registration_date
        }
    
    def __repr__(self):
        return f"Farmer(id={self.farmer_id}, name='{self.name}', location='{self.location}')"


class Worker:
    """
    Worker data model class.
    
    Represents a worker who can be matched to jobs.
    """
    
    def __init__(self, name, phone, location, skills, available=True, worker_id=None, registration_date=None):
        """
        Initialize Worker instance.
        
        Args:
            name (str): Worker's full name
            phone (str): Phone number
            location (str): Location/address
            skills (str): Comma-separated skills
            available (bool): Availability status
            worker_id (int, optional): Database ID
            registration_date (str, optional): Registration timestamp
        """
        self.worker_id = worker_id
        self.name = name
        self.phone = phone
        self.location = location
        self.skills = skills
        self.available = available
        self.registration_date = registration_date
    
    def validate(self):
        """
        Validate worker data.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.name or len(self.name.strip()) == 0:
            return False, "Name is required"
        
        if not validate_phone(self.phone):
            return False, "Invalid phone number format"
        
        if not validate_location(self.location):
            return False, "Invalid location"
        
        if not self.skills or len(self.skills.strip()) == 0:
            return False, "Skills are required"
        
        return True, None
    
    def get_skills_list(self):
        """
        Get skills as a list.
        
        Returns:
            list: List of skill strings
        """
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    def has_skill(self, skill):
        """
        Check if worker has a specific skill.
        
        Args:
            skill (str): Skill to check for
            
        Returns:
            bool: True if worker has the skill
        """
        skills_list = self.get_skills_list()
        return skill.lower().strip() in [s.lower() for s in skills_list]
    
    def to_dict(self):
        """
        Convert worker instance to dictionary.
        
        Returns:
            dict: Dictionary representation of worker
        """
        return {
            'worker_id': self.worker_id,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'skills': self.skills,
            'available': self.available,
            'registration_date': self.registration_date
        }
    
    def __repr__(self):
        return f"Worker(id={self.worker_id}, name='{self.name}', location='{self.location}', available={self.available})"


class Job:
    """
    Job data model class.
    
    Represents a job posting by a farmer.
    """
    
    def __init__(self, farmer_id, title, skill_required, location, description=None, 
                 duration=None, pay_rate=None, status='open', job_id=None, posted_date=None):
        """
        Initialize Job instance.
        
        Args:
            farmer_id (int): ID of the farmer posting the job
            title (str): Job title
            skill_required (str): Required skill for the job
            location (str): Job location
            description (str, optional): Job description
            duration (str, optional): Job duration
            pay_rate (str, optional): Pay rate information
            status (str): Job status (open/filled/closed)
            job_id (int, optional): Database ID
            posted_date (str, optional): Posting timestamp
        """
        self.job_id = job_id
        self.farmer_id = farmer_id
        self.title = title
        self.description = description
        self.skill_required = skill_required
        self.location = location
        self.duration = duration
        self.pay_rate = pay_rate
        self.status = status
        self.posted_date = posted_date
    
    def validate(self):
        """
        Validate job data.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.farmer_id or not isinstance(self.farmer_id, int):
            return False, "Farmer ID is required"
        
        if not self.title or len(self.title.strip()) == 0:
            return False, "Job title is required"
        
        if not self.skill_required or len(self.skill_required.strip()) == 0:
            return False, "Required skill is needed"
        
        if not validate_location(self.location):
            return False, "Invalid location"
        
        if self.status not in ['open', 'filled', 'closed']:
            return False, "Status must be 'open', 'filled', or 'closed'"
        
        return True, None
    
    def to_dict(self):
        """
        Convert job instance to dictionary.
        
        Returns:
            dict: Dictionary representation of job
        """
        return {
            'job_id': self.job_id,
            'farmer_id': self.farmer_id,
            'title': self.title,
            'description': self.description,
            'skill_required': self.skill_required,
            'location': self.location,
            'duration': self.duration,
            'pay_rate': self.pay_rate,
            'status': self.status,
            'posted_date': self.posted_date
        }
    
    def __repr__(self):
        return f"Job(id={self.job_id}, title='{self.title}', location='{self.location}', status='{self.status}')"
