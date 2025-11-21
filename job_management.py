"""
Job management module for Local Agricultural Job Board & Skills Matcher

This module handles job posting, viewing, searching, and management operations.
Owner: Sylvie Uwera
"""

import database
from tabulate import tabulate
from models import Job, validate_location
from utils import print_error, print_success, print_info


def post_job(farmer_id: int):
    """
    Post a new job for a specific farmer.
    
    Args:
        farmer_id (int): ID of the farmer posting the job
    """
    print("\n--- Post a New Job ---")
    
    title = input("Enter job title: ").strip()
    if not title:
        print_error("Job title is required.")
        return
    
    description = input("Enter job description (optional): ").strip() or None
    
    skill_required = input("Enter required skill: ").strip()
    if not skill_required:
        print_error("Required skill is needed.")
        return
    
    location = input("Enter job location: ").strip()
    if not validate_location(location):
        print_error("Invalid location.")
        return
    
    duration = input("Enter job duration (optional): ").strip() or None
    pay_rate = input("Enter pay rate (optional): ").strip() or None
    
    # Create job model and validate
    job = Job(
        farmer_id=farmer_id,
        title=title,
        description=description,
        skill_required=skill_required,
        location=location,
        duration=duration,
        pay_rate=pay_rate,
        status='open'
    )
    
    is_valid, error = job.validate()
    if not is_valid:
        print_error(error)
        return
    
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO jobs (farmer_id, title, description, skill_required, location, duration, pay_rate, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (job.farmer_id, job.title, job.description, job.skill_required, 
             job.location, job.duration, job.pay_rate, job.status)
        )
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        
        print_success(f"Job posted successfully! Job ID: {job_id}")
    except Exception as e:
        print_error(f"Failed to post job: {e}")


def view_all_jobs():
    """Display all jobs in a formatted table."""
    jobs = database.fetch_all("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        ORDER BY posted_date DESC
    """)
    
    if not jobs:
        print_info("No jobs found.")
        return
    
    # Convert to list of lists for tabulate
    table_data = []
    for job in jobs:
        table_data.append([
            job['job_id'],
            job['title'],
            job['skill_required'],
            job['location'],
            job['duration'] or 'N/A',
            job['pay_rate'] or 'N/A',
            job['status'],
            job['posted_date'] or 'N/A'
        ])
    
    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def view_farmer_jobs(farmer_id: int):
    """Display jobs posted by a specific farmer."""
    jobs = database.fetch_all(
        """
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE farmer_id = ?
        ORDER BY posted_date DESC
        """,
        (farmer_id,)
    )
    
    if not jobs:
        print_info("You have no jobs posted.")
        return
    
    # Convert to list of lists for tabulate
    table_data = []
    for job in jobs:
        table_data.append([
            job['job_id'],
            job['title'],
            job['skill_required'],
            job['location'],
            job['duration'] or 'N/A',
            job['pay_rate'] or 'N/A',
            job['status'],
            job['posted_date'] or 'N/A'
        ])
    
    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def search_jobs_by_location(location: str):
    """Search and display jobs by location."""
    if not location or not location.strip():
        print_error("Location cannot be empty.")
        return
    
    location_pattern = f"%{location.strip()}%"
    jobs = database.fetch_all(
        """
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE location LIKE ?
        ORDER BY posted_date DESC
        """,
        (location_pattern,)
    )
    
    if not jobs:
        print_info(f"No jobs found in '{location}'.")
        return
    
    # Convert to list of lists for tabulate
    table_data = []
    for job in jobs:
        table_data.append([
            job['job_id'],
            job['title'],
            job['skill_required'],
            job['location'],
            job['duration'] or 'N/A',
            job['pay_rate'] or 'N/A',
            job['status'],
            job['posted_date'] or 'N/A'
        ])
    
    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def update_job_status(job_id: int, new_status: str):
    """Update a job's status (open/filled/closed)."""
    new_status = new_status.lower()
    if new_status not in ("open", "filled", "closed"):
        print_error("Invalid status. Must be 'open', 'filled', or 'closed'.")
        return
    
    # Check if job exists
    job = database.fetch_one("SELECT job_id FROM jobs WHERE job_id = ?", (job_id,))
    if not job:
        print_error(f"Job with ID {job_id} not found.")
        return
    
    try:
        database.execute_query(
            "UPDATE jobs SET status = ? WHERE job_id = ?",
            (new_status, job_id)
        )
        print_success(f"Job status updated to '{new_status}'.")
    except Exception as e:
        print_error(f"Failed to update job status: {e}")


def delete_job(job_id: int):
    """Delete a job from the database."""
    # Check if job exists
    job = database.fetch_one("SELECT job_id, title FROM jobs WHERE job_id = ?", (job_id,))
    if not job:
        print_error(f"Job with ID {job_id} not found.")
        return
    
    try:
        database.execute_query("DELETE FROM jobs WHERE job_id = ?", (job_id,))
        print_success(f"Job '{job.get('title', job_id)}' deleted successfully.")
    except Exception as e:
        print_error(f"Failed to delete job: {e}")


__all__ = [
    "post_job",
    "view_all_jobs",
    "view_farmer_jobs",
    "update_job_status",
    "delete_job",
    "search_jobs_by_location",
]
