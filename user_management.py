import uuid

# In-memory storage
farmers = {}
workers = {}


# ------------------------------
# Validation Utilities
# ------------------------------
def validate_non_empty(value, field_name="Field"):
    """Ensure the input is not empty."""
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def validate_integer(value, field_name="Field"):
    """Ensure the input can be converted to an integer."""
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number.")


def validate_phone(phone):
    """Ensure phone number contains digits only and has at least 7 characters."""
    phone = phone.strip()

    if not phone.isdigit() or len(phone) < 7:
        raise ValueError("Phone number must contain digits only and be at least 7 characters.")
    return phone


# ------------------------------
# Helper Functions
# ------------------------------
def generate_id():
    """Generate a short unique ID."""
    return str(uuid.uuid4())[:8]


def save_profile(user_type, user_id, data):
    """Save farmer or worker profile."""
    if user_type == "farmer":
        farmers[user_id] = data
    elif user_type == "worker":
        workers[user_id] = data


def get_profile(user_type, user_id):
    """Retrieve stored profile."""
    if user_type == "farmer":
        return farmers.get(user_id)
    elif user_type == "worker":
        return workers.get(user_id)
    return None


# ------------------------------
# Registration Functions
# ------------------------------
def register_farmer():
    print("\n=== Farmer Registration ===")
    try:
        name = validate_non_empty(input("Enter your full name: "), "Name")
        location = validate_non_empty(input("Enter your location: "), "Location")
        farm_size = validate_non_empty(input("Enter farm size (e.g., '3 acres'): "), "Farm Size")
        crops = validate_non_empty(input("Crops grown (comma separated): "), "Crops")
        phone = validate_phone(input("Phone number: "))

        user_id = generate_id()

        profile_data = {
            "id": user_id,
            "name": name,
            "location": location,
            "farm_size": farm_size,
            "crops": [c.strip() for c in crops.split(",")],
            "phone": phone
        }

        save_profile("farmer", user_id, profile_data)

        print(f"\nFarmer registered successfully! Your ID is: {user_id}")
        return user_id

    except ValueError as e:
        print("Error:", e)
        return None


def register_worker():
    print("\n=== Worker Registration ===")
    try:
        name = validate_non_empty(input("Enter your full name: "), "Name")
        age = validate_integer(input("Enter your age: "), "Age")
        skills = validate_non_empty(input("Skills (comma separated): "), "Skills")
        availability = validate_non_empty(input("Availability (e.g., Full-time): "), "Availability")
        phone = validate_phone(input("Phone number: "))

        user_id = generate_id()

        profile_data = {
            "id": user_id,
            "name": name,
            "age": age,
            "skills": [s.strip() for s in skills.split(",")],
            "availability": availability,
            "phone": phone
        }

        save_profile("worker", user_id, profile_data)

        print(f"\nWorker registered successfully! Your ID is: {user_id}")
        return user_id

    except ValueError as e:
        print("Error:", e)
        return None


# ------------------------------
# Profile Viewing & Updating
# ------------------------------
def view_profile(user_type, user_id):
    profile = get_profile(user_type, user_id)
    if not profile:
        print("Profile not found.")
        return

    print(f"\n=== {user_type.capitalize()} Profile ===")
    for key, value in profile.items():
        print(f"{key.capitalize()}: {value}")


def update_profile(user_type, user_id):
    profile = get_profile(user_type, user_id)
    if not profile:
        print("Profile not found.")
        return

    print("\nWhich field would you like to update?")
    for key in profile.keys():
        if key != "id":
            print(f"- {key}")

    field = input("\nEnter field name: ").strip()

    if field not in profile or field == "id":
        print("Invalid field selected.")
        return

    new_value = input(f"Enter new value for {field}: ")

    try:
        # Validation based on existing field type
        if field == "phone":
            new_value = validate_phone(new_value)
        elif isinstance(profile[field], int):
            new_value = validate_integer(new_value, field)
        elif isinstance(profile[field], list):
            new_value = [v.strip() for v in new_value.split(",")]
        else:
            new_value = validate_non_empty(new_value, field)

        profile[field] = new_value
        save_profile(user_type, user_id, profile)

        print("Profile updated successfully!")

    except ValueError as e:
        print("Error:", e)


# ------------------------------
# Authentication & User Type Selection
# ------------------------------
def choose_user_type():
    print("\nAre you a:")
    print("1. Farmer")
    print("2. Worker")

    choice = input("Select 1 or 2: ")

    if choice == "1":
        return "farmer"
    elif choice == "2":
        return "worker"
    else:
        print("Invalid selection.")
        return None


def authenticate_user():
    print("\n=== User Login ===")
    user_type = choose_user_type()
    if not user_type:
        return None, None

    user_id = input("Enter your user ID: ").strip()

    if get_profile(user_type, user_id):
        print("Login successful!")
        return user_type, user_id
    else:
        print("Invalid ID.")
        return None, None


# ------------------------------
# CLI Menu
# ------------------------------
if __name__ == "__main__":
    while True:
        print("\n=== User Management Menu ===")
        print("1. Register Farmer")
        print("2. Register Worker")
        print("3. Login & View Profile")
        print("4. Login & Update Profile")
        print("5. Exit")

        option = input("Choose an option: ")

        if option == "1":
            register_farmer()
        elif option == "2":
            register_worker()
        elif option == "3":
            u_type, u_id = authenticate_user()
            if u_type:
                view_profile(u_type, u_id)
        elif option == "4":
            u_type, u_id = authenticate_user()
            if u_type:
                update_profile(u_type, u_id)
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
