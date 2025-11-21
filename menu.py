

from utils import clear_screen, print_header, print_separator, print_error


def display_main_menu():
    
    clear_screen()
    print_header("Local Agricultural Job Board & Skills Match making system")
    
    print("MAIN MENU")
    print_separator()
    print("[1] Register as Farmer")
    print("[2] Register as Worker")
    print("[3] Login as Farmer")
    print("[4] Login as Worker")
    print("[5] View Available Jobs")
    print("[6] Search Jobs by Location")
    print("[7] Exit")
    print_separator()
    
    return get_user_choice(1, 7)


def display_farmer_menu(farmer_name):
    
    clear_screen()
    print_header(f"Farmer Dashboard - Welcome, {farmer_name}!")
    
    print("FARMER MENU")
    print_separator()
    print("[1] View My Profile")
    print("[2] Post a New Job")
    print("[3] View My Posted Jobs")
    print("[4] Find Workers for a Job")
    print("[5] Update Job Status")
    print("[6] Delete a Job")
    print("[7] Back to Main Menu")
    print_separator()
    
    return get_user_choice(1, 7)


def display_worker_menu(worker_name):
   
    clear_screen()
    print_header(f"Worker Dashboard - Welcome, {worker_name}!")
    
    print("WORKER MENU")
    print_separator()
    print("[1] View My Profile")
    print("[2] Update My Skills")
    print("[3] Update Availability Status")
    print("[4] View All Available Jobs")
    print("[5] Find Jobs Matching My Skills")
    print("[6] Search Jobs by Location")
    print("[7] Back to Main Menu")
    print_separator()
    
    return get_user_choice(1, 7)


def display_login_menu(user_type):
    
    clear_screen()
    print_header(f"{user_type.capitalize()} Login")
    
    print(f"Please select a {user_type} to continue:")
    print_separator()
    
    return None  


def get_user_choice(min_option, max_option):
    
    while True:
        try:
            choice = int(input(f"\nEnter your choice ({min_option}-{max_option}): "))
            
            if min_option <= choice <= max_option:
                return choice
            else:
                print_error(f"Please enter a number between {min_option} and {max_option}.")
        except ValueError:
            print_error("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            exit(0)


def display_job_status_menu():
    
    print("\nSelect new job status:")
    print_separator()
    print("[1] Open")
    print("[2] Filled")
    print("[3] Closed")
    print_separator()
    
    choice = get_user_choice(1, 3)
    
    status_map = {
        1: 'open',
        2: 'filled',
        3: 'closed'
    }
    
    return status_map[choice]


def display_welcome_message():
   
    clear_screen()
    print("\n")
    print("=" * 60)
    print("  WELCOME TO LOCAL AGRICULTURAL JOB BOARD")
    print("  Connecting Farmers with Skilled Agricultural Workers")
    print("=" * 60)
    print("\n  This system helps:")
    print("  • Farmers find qualified workers for their farms")
    print("  • Workers discover job opportunities in agriculture")
    print("  • Match jobs with workers based on skills and location")
    print("\n" + "=" * 60 + "\n")
    input("Press Enter to continue...")


def display_exit_message():
    
    clear_screen()
    print_header("Thank You!")
    print("Thank you for using the Agricultural Job Board.")
    print("Helping farmers and workers connect for a better harvest!")
    print("\nGoodbye! \n")