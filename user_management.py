import database
from models import Farmer, Worker
from utils import (
    print_error,
    print_success,
    print_info,
)


# ------------------------------
# Registration Functions (DB-backed)
# ------------------------------
def register_farmer():
    """
    Register a farmer and save to the SQLite database.

    This implementation is aligned with the `farmers` table defined in `database.py`.
    """
    print("\n=== Farmer Registration ===")

    name = input("Enter your full name: ").strip()
    phone = input("Enter your phone number: ").strip()
    location = input("Enter your location: ").strip()
    email = input("Enter your email (optional): ").strip() or None

    farmer = Farmer(name=name, phone=phone, location=location, email=email)
    is_valid, error = farmer.validate()
    if not is_valid:
        print_error(error)
        return None

    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO farmers (name, phone, location, email)
            VALUES (?, ?, ?, ?)
            """,
            (farmer.name, farmer.phone, farmer.location, farmer.email),
        )
        conn.commit()
        farmer_id = cursor.lastrowid
        conn.close()

        print_success(f"Farmer registered successfully! Your ID is: {farmer_id}")
        return farmer_id
    except Exception as e:
        print_error(f"Failed to register farmer: {e}")
        return None


def register_worker():
    """
    Register a worker and save to the SQLite database.

    This implementation is aligned with the `workers` table defined in `database.py`.
    """
    print("\n=== Worker Registration ===")

    name = input("Enter your full name: ").strip()
    phone = input("Enter your phone number: ").strip()
    location = input("Enter your location: ").strip()
    skills = input("Skills (comma separated): ").strip()

    availability_input = input("Are you currently available for work? (y/n): ").strip().lower()
    available = availability_input in ("y", "yes")

    worker = Worker(name=name, phone=phone, location=location, skills=skills, available=available)
    is_valid, error = worker.validate()
    if not is_valid:
        print_error(error)
        return None

    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO workers (name, phone, location, skills, available)
            VALUES (?, ?, ?, ?, ?)
            """,
            (worker.name, worker.phone, worker.location, worker.skills, int(worker.available)),
        )
        conn.commit()
        worker_id = cursor.lastrowid
        conn.close()

        print_success(f"Worker registered successfully! Your ID is: {worker_id}")
        return worker_id
    except Exception as e:
        print_error(f"Failed to register worker: {e}")
        return None


# ------------------------------
# Profile Viewing & Updating (DB-backed)
# ------------------------------
def view_farmer_profile(farmer_id: int):
    """Display a farmer profile from the database."""
    farmer = database.fetch_one("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
    if not farmer:
        print_info("Farmer profile not found.")
        return

    print("\n=== Farmer Profile ===")
    for key in ("farmer_id", "name", "phone", "location", "email", "registration_date"):
        if key in farmer:
            print(f"{key.replace('_', ' ').title()}: {farmer[key]}")


def view_worker_profile(worker_id: int):
    """Display a worker profile from the database."""
    worker = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
    if not worker:
        print_info("Worker profile not found.")
        return

    print("\n=== Worker Profile ===")
    for key in ("worker_id", "name", "phone", "location", "skills", "available", "registration_date"):
        if key in worker:
            print(f"{key.replace('_', ' ').title()}: {worker[key]}")


def update_worker_skills(worker_id: int):
    """Prompt for and update a worker's skills in the database."""
    worker = database.fetch_one("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
    if not worker:
        print_info("Worker profile not found.")
        return

    print(f"Current skills: {worker.get('skills', '')}")
    new_skills = input("Enter new skills (comma separated): ").strip()
    if not new_skills:
        print_error("Skills cannot be empty.")
        return

    try:
        database.execute_query(
            "UPDATE workers SET skills = ? WHERE worker_id = ?",
            (new_skills, worker_id),
        )
        print_success("Worker skills updated successfully!")
    except Exception as e:
        print_error(f"Failed to update skills: {e}")


def update_availability(worker_id: int, available: bool):
    """Update a worker's availability flag in the database."""
    try:
        database.execute_query(
            "UPDATE workers SET available = ? WHERE worker_id = ?",
            (1 if available else 0, worker_id),
        )
        status_text = "available" if available else "not available"
        print_success(f"Availability updated: worker is now {status_text}.")
    except Exception as e:
        print_error(f"Failed to update availability: {e}")


# ------------------------------
__all__ = [
    "register_farmer",
    "register_worker",
    "view_farmer_profile",
    "view_worker_profile",
    "update_worker_skills",
    "update_availability",
]
