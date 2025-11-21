
import sys
from utils import (
    clear_screen, print_header, print_separator, 
    print_success, print_error, print_info, pause, confirm_action
)
from menu import (
    display_main_menu, display_farmer_menu, display_worker_menu,
    display_welcome_message, display_exit_message, get_user_choice
)

try:
    import database
    import user_management
    import job_management
    import matching_engine
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required modules are in the same directory.")
    sys.exit(1)


def initialize_system():
    
    try:
        print_info("Initializing database...")
        database.init_database()
        print_success("Database initialized successfully!")
        return True
    except Exception as e:
        print_error(f"Failed to initialize database: {e}")
        return False


def handle_farmer_registration():
    try:
        clear_screen()
        print_header("Farmer Registration")
        user_management.register_farmer()
        pause()
    except Exception as e:
        print_error(f"Registration failed: {e}")
        pause()


def handle_worker_registration():
    try:
        clear_screen()
        print_header("Worker Registration")
        user_management.register_worker()
        pause()
    except Exception as e:
        print_error(f"Registration failed: {e}")
        pause()


def handle_farmer_login():
    
    try:
        clear_screen()
        print_header("Farmer Login")
        
        farmers = database.fetch_all("SELECT farmer_id, name, location FROM farmers")
        
        if not farmers:
            print_info("No farmers registered yet. Please register first.")
            pause()
            return True
        
        print("Available Farmers:")
        print_separator()
        for idx, farmer in enumerate(farmers, 1):
            print(f"[{idx}] {farmer['name']} - {farmer['location']}")
        print_separator()
        
        choice = get_user_choice(1, len(farmers))
        selected_farmer = farmers[choice - 1]
        farmer_id = selected_farmer["farmer_id"]
        farmer_name = selected_farmer["name"]
        
        while True:
            choice = display_farmer_menu(farmer_name)
            
            if choice == 1:
                clear_screen()
                print_header("My Profile")
                user_management.view_farmer_profile(farmer_id)
                pause()
                
            elif choice == 2:
                clear_screen()
                print_header("Post New Job")
                job_management.post_job(farmer_id)
                pause()
                
            elif choice == 3:
                clear_screen()
                print_header("My Posted Jobs")
                job_management.view_farmer_jobs(farmer_id)
                pause()
                
            elif choice == 4:
                clear_screen()
                print_header("Find Workers")
                jobs = database.fetch_all(
                    "SELECT job_id, title FROM jobs WHERE farmer_id = ? AND status = 'open'",
                    (farmer_id,)
                )
                
                if not jobs:
                    print_info("You have no open jobs.")
                    pause()
                    continue
                
                print("Your Open Jobs:")
                print_separator()
                for idx, job in enumerate(jobs, 1):
                    print(f"[{idx}] {job['title']}")
                print_separator()
                
                job_choice = get_user_choice(1, len(jobs))
                job_id = jobs[job_choice - 1]["job_id"]
                
                matching_engine.match_workers_to_job(job_id)
                pause()
                
            elif choice == 5:
                clear_screen()
                print_header("Update Job Status")
                jobs = database.fetch_all(
                    "SELECT job_id, title, status FROM jobs WHERE farmer_id = ?",
                    (farmer_id,)
                )
                
                if not jobs:
                    print_info("You have no jobs posted.")
                    pause()
                    continue
                
                print("Your Jobs:")
                print_separator()
                for idx, job in enumerate(jobs, 1):
                    print(f"[{idx}] {job['title']} (Status: {job['status']})")
                print_separator()
                
                job_choice = get_user_choice(1, len(jobs))
                job_id = jobs[job_choice - 1]["job_id"]
                
                from menu import display_job_status_menu
                new_status = display_job_status_menu()
                
                job_management.update_job_status(job_id, new_status)
                pause()
                
            elif choice == 6:
                clear_screen()
                print_header("Delete Job")
                jobs = database.fetch_all(
                    "SELECT job_id, title FROM jobs WHERE farmer_id = ?",
                    (farmer_id,)
                )
                
                if not jobs:
                    print_info("You have no jobs to delete.")
                    pause()
                    continue
                
                print("Your Jobs:")
                print_separator()
                for idx, job in enumerate(jobs, 1):
                    print(f"[{idx}] {job['title']}")
                print_separator()
                
                job_choice = get_user_choice(1, len(jobs))
                job_id = jobs[job_choice - 1]["job_id"]
                
                if confirm_action("Are you sure you want to delete this job?"):
                    job_management.delete_job(job_id)
                    pause()
                
            elif choice == 7:
                break
                
        return True
        
    except Exception as e:
        print_error(f"An error occurred: {e}")
        pause()
        return True


def handle_worker_login():
   
    try:
        clear_screen()
        print_header("Worker Login")
        
        workers = database.fetch_all("SELECT worker_id, name, skills FROM workers")
        
        if not workers:
            print_info("No workers registered yet. Please register first.")
            pause()
            return True
        
        print("Available Workers:")
        print_separator()
        for idx, worker in enumerate(workers, 1):
            print(f"[{idx}] {worker['name']} - Skills: {worker['skills']}")
        print_separator()
        
        choice = get_user_choice(1, len(workers))
        selected_worker = workers[choice - 1]
        worker_id = selected_worker["worker_id"]
        worker_name = selected_worker["name"]
        
        while True:
            choice = display_worker_menu(worker_name)
            
            if choice == 1:
                clear_screen()
                print_header("My Profile")
                user_management.view_worker_profile(worker_id)
                pause()
                
            elif choice == 2:
                clear_screen()
                print_header("Update Skills")
                user_management.update_worker_skills(worker_id)
                pause()
                
            elif choice == 3:
                clear_screen()
                print_header("Update Availability")
                print("Are you currently available for work?")
                print("[1] Yes - Available")
                print("[2] No - Not Available")
                status_choice = get_user_choice(1, 2)
                available = True if status_choice == 1 else False
                user_management.update_availability(worker_id, available)
                pause()
                
            elif choice == 4:
                clear_screen()
                print_header("All Available Jobs")
                job_management.view_all_jobs()
                pause()
                
            elif choice == 5:
                clear_screen()
                print_header("Jobs Matching Your Skills")
                matching_engine.match_jobs_to_worker(worker_id)
                pause()
                
            elif choice == 6:
                clear_screen()
                print_header("Search Jobs by Location")
                location = input("Enter location: ").strip()
                job_management.search_jobs_by_location(location)
                pause()
                
            elif choice == 7:
                break
                
        return True
        
    except Exception as e:
        print_error(f"An error occurred: {e}")
        pause()
        return True


def handle_view_jobs():
    try:
        clear_screen()
        print_header("All Available Jobs")
        job_management.view_all_jobs()
        pause()
    except Exception as e:
        print_error(f"Failed to display jobs: {e}")
        pause()


def handle_search_jobs():
    try:
        clear_screen()
        print_header("Search Jobs by Location")
        location = input("Enter location to search: ").strip()
        
        if location:
            job_management.search_jobs_by_location(location)
        else:
            print_error("Location cannot be empty.")
            
        pause()
    except Exception as e:
        print_error(f"Search failed: {e}")
        pause()


def main():
    
    if not initialize_system():
        print_error("System initialization failed. Exiting...")
        sys.exit(1)
    
    display_welcome_message()
    
    while True:
        try:
            choice = display_main_menu()
            
            if choice == 1:
                handle_farmer_registration()
                
            elif choice == 2:
                handle_worker_registration()
                
            elif choice == 3:
                handle_farmer_login()
                
            elif choice == 4:
                handle_worker_login()
                
            elif choice == 5:
                handle_view_jobs()
                
            elif choice == 6:
                handle_search_jobs()
                
            elif choice == 7:
                if confirm_action("Are you sure you want to exit?"):
                    display_exit_message()
                    break
                    
        except KeyboardInterrupt:
            print("\n")
            if confirm_action("Are you sure you want to exit?"):
                display_exit_message()
                break
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
            pause()


if __name__ == "__main__":
    main()