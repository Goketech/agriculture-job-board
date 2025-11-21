import sqlite3
from tabulate import tabulate

DB_NAME = "data/agri_jobs.db"


# 1. Add a new job (internal helper)
def _add_job_with_farmer(farmer_id: int):
    """Internal helper to add a new job for a given farmer_id."""
    print("\n--- Add a New Job ---")
    title = input("Enter job title: ").strip()
    skill_required = input("Enter required skill: ").strip()
    location = input("Enter job location: ").strip()
    duration = input("Enter job duration: ").strip()
    pay_rate = input("Enter pay rate: ").strip()
    status = input("Enter job status (open/filled/closed) [open]: ").strip().lower() or "open"

    if status not in ("open", "filled", "closed"):
        print("Invalid status. Must be 'open', 'filled', or 'closed'.")
        return

    if not all([title, skill_required, location, duration, pay_rate]):
        print("All fields are required!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (farmer_id, title, skill_required, location, duration, pay_rate, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (farmer_id, title, skill_required, location, duration, pay_rate, status),
    )

    conn.commit()
    conn.close()
    print("Job added successfully!")


def post_job(farmer_id: int):
    """Public API used by main.py to post a job for a specific farmer."""
    _add_job_with_farmer(farmer_id)

# 2. View all jobs
def view_all_jobs():
    """Display all jobs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
    """)
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print("No jobs found.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))

# 3. View jobs by location
def view_jobs_by_location():
    location_input = input("Enter location to filter jobs: ").strip()
    if not location_input:
        print("Invalid input.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE location LIKE ?
    """, (f"%{location_input}%",))
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"No jobs found in '{location_input}'.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))
# 4. View jobs by skill
def view_jobs_by_skill():
    """Function to display jobs filtered by skill."""
    skill_input = input("Enter skill to filter jobs: ").strip()
    if not skill_input:
        print("Invalid input. Please enter a skill.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE skill_required LIKE ?
    """, (f"%{skill_input}%",))
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"No jobs found requiring '{skill_input}'.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))


# 5. View jobs by title
def view_jobs_by_title():
    """Function to display jobs filtered by title."""
    title_input = input("Enter job title to search: ").strip()
    if not title_input:
        print("Invalid input. Please enter a title.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE title LIKE ?
    """, (f"%{title_input}%",))
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"No jobs found with title '{title_input}'.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))

# 6. View jobs by status
def view_jobs_by_status():
    """Function to display jobs filtered by status."""
    status_input = input("Enter job status (open/closed): ").strip().lower()
    if status_input not in ["open", "closed"]:
        print("Invalid status. Choose 'open' or 'closed'.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE status = ?
    """, (status_input,))
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"No jobs found with status '{status_input}'.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))

DB_NAME = "data/agri_jobs.db"

def update_job():
    """Function to update an existing job's details safely."""
    try:
        job_id = int(input("Enter the Job ID to update: "))
    except ValueError:
        print("Invalid Job ID. Must be a number.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #  Use the correct primary key column name (job_id)
    cursor.execute("SELECT job_id, title, skill_required, location, duration, pay_rate, status FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        print(f"No job found with ID {job_id}.")
        conn.close()
        return

    current_id, current_title, current_skill, current_location, current_duration, current_pay, current_status = job

    print("Leave a field blank if you do not want to change it.")

    #  Prompt user with current values, keep if blank
    title = input(f"Enter new title [{current_title}]: ").strip() or current_title
    skill_required = input(f"Enter new skill required [{current_skill or 'N/A'}]: ").strip() or current_skill or 'N/A'
    location = input(f"Enter new location [{current_location}]: ").strip() or current_location
    duration = input(f"Enter new duration [{current_duration}]: ").strip() or current_duration

    #  Validate pay rate as float
    pay_input = input(f"Enter new pay rate [{current_pay}]: ").strip()
    try:
        pay_rate = float(pay_input) if pay_input else current_pay
    except ValueError:
        print("Invalid pay rate. Must be a number.")
        conn.close()
        return

    #  Validate status (only open/closed allowed)
    status_input = input(f"Enter new status (open/closed) [{current_status}]: ").strip().lower()
    status = status_input if status_input in ["open", "closed"] else current_status

    try:
        cursor.execute("""
            UPDATE jobs
            SET title = ?, skill_required = ?, location = ?, duration = ?, pay_rate = ?, status = ?
            WHERE job_id = ?
        """, (title, skill_required, location, duration, pay_rate, status, job_id))
        conn.commit()

        #  Show updated job in a clean table
        cursor.execute("SELECT job_id, title, skill_required, location, duration, pay_rate, status FROM jobs WHERE job_id = ?", (job_id,))
        updated_job = cursor.fetchone()
        print(f"\n  Job ID {job_id} has been updated successfully.\n")
        print(tabulate([updated_job], headers=["Job ID", "Title", "Skill Required", "Location", "Duration", "Pay Rate", "Status"], tablefmt="grid"))

    except sqlite3.IntegrityError as e:
        print("An error occurred:", e)
    finally:
        conn.close()


def delete_job(job_id: int | None = None):
    """Function to safely delete a job from the database.

    If job_id is None, prompt the user (backwards compatible);
    otherwise delete the given job_id (used by main.py).
    """
    if job_id is None:
        try:
            job_id = int(input("Enter the Job ID to delete: "))
        except ValueError:
            print("Invalid Job ID. Must be a number.")
            return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        print(f"No job found with ID {job_id}.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete job '{job[2]}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
        conn.commit()
        print(f"Job ID {job_id} has been deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def view_farmer_jobs(farmer_id: int):
    """Display jobs posted by a specific farmer (used by main.py)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE farmer_id = ?
        """,
        (farmer_id,),
    )
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print("You have no jobs posted.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))


def update_job_status(job_id: int, new_status: str):
    """Update a job's status (open/filled/closed)."""
    new_status = new_status.lower()
    if new_status not in ("open", "filled", "closed"):
        print("Invalid status. Must be 'open', 'filled', or 'closed'.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (new_status, job_id))
    conn.commit()
    conn.close()
    print(f"Job status updated to '{new_status}'.")


def search_jobs_by_location(location: str):
    """Search and display jobs by a given location string (used by main.py)."""
    location_input = location.strip()
    if not location_input:
        print("Invalid input.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT job_id, title, skill_required, location, duration, pay_rate, status, posted_date
        FROM jobs
        WHERE location LIKE ?
        """,
        (f"%{location_input}%",),
    )
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"No jobs found in '{location_input}'.")
        return

    headers = ["Job ID", "Title", "Skills Required", "Location", "Duration", "Pay Rate", "Status", "Posted Date"]
    print(tabulate(jobs, headers=headers, tablefmt="grid"))


__all__ = [
    "post_job",
    "view_all_jobs",
    "view_farmer_jobs",
    "update_job_status",
    "delete_job",
    "search_jobs_by_location",
]

