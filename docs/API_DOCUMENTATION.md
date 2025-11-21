# API Documentation - Local Agricultural Job Board & Skills Matcher

## Table of Contents

1. [Database Module](#database-module)
2. [Models Module](#models-module)
3. [User Management Module](#user-management-module)
4. [Job Management Module](#job-management-module)
5. [Matching Engine Module](#matching-engine-module)
6. [Menu Module](#menu-module)
7. [Utils Module](#utils-module)

## Database Module

### `init_database()`

Creates the database directory and initializes all tables.

**Returns:**
- `bool`: True if successful, False otherwise

**Raises:**
- `sqlite3.Error`: If database operations fail

**Example:**
```python
import database
success = database.init_database()
```

### `get_connection()`

Returns a database connection object with Row factory enabled.

**Returns:**
- `sqlite3.Connection`: Database connection object

**Raises:**
- `sqlite3.Error`: If connection fails

**Example:**
```python
conn = database.get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM farmers")
conn.close()
```

### `execute_query(query, params=None)`

Execute a SQL query safely with parameter binding.

**Parameters:**
- `query` (str): SQL query string
- `params` (tuple, optional): Parameters for the query

**Returns:**
- `sqlite3.Cursor`: Cursor object with executed query

**Raises:**
- `sqlite3.Error`: If query execution fails

**Example:**
```python
database.execute_query(
    "INSERT INTO farmers (name, phone, location) VALUES (?, ?, ?)",
    ("John Doe", "1234567890", "Kigali, Rwanda")
)
```

### `fetch_all(query, params=None)`

Fetch all results from a query.

**Parameters:**
- `query` (str): SQL query string
- `params` (tuple, optional): Parameters for the query

**Returns:**
- `list`: List of dictionaries representing rows, or empty list on error

**Example:**
```python
farmers = database.fetch_all("SELECT * FROM farmers")
for farmer in farmers:
    print(farmer['name'])
```

### `fetch_one(query, params=None)`

Fetch a single result from a query.

**Parameters:**
- `query` (str): SQL query string
- `params` (tuple, optional): Parameters for the query

**Returns:**
- `dict`: Dictionary representing the row, or None if not found or on error

**Example:**
```python
farmer = database.fetch_one(
    "SELECT * FROM farmers WHERE farmer_id = ?",
    (1,)
)
if farmer:
    print(farmer['name'])
```

## Models Module

### Validation Functions

#### `validate_phone(phone)`

Validate phone number format.

**Parameters:**
- `phone` (str): Phone number to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from models import validate_phone
is_valid = validate_phone("123-456-7890")  # True
```

#### `validate_email(email)`

Validate email format using regex.

**Parameters:**
- `email` (str): Email address to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from models import validate_email
is_valid = validate_email("user@example.com")  # True
```

#### `validate_location(location)`

Validate location input.

**Parameters:**
- `location` (str): Location to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from models import validate_location
is_valid = validate_location("Kigali, Rwanda")  # True
```

### Model Classes

#### `Farmer`

Represents a farmer who can post jobs.

**Constructor:**
```python
Farmer(name, phone, location, email=None, farmer_id=None, registration_date=None)
```

**Methods:**
- `validate()`: Returns `(bool, str)` - (is_valid, error_message)
- `to_dict()`: Returns dictionary representation

**Example:**
```python
from models import Farmer

farmer = Farmer(
    name="John Doe",
    phone="1234567890",
    location="Kigali, Rwanda",
    email="john@example.com"
)

is_valid, error = farmer.validate()
if is_valid:
    print("Farmer is valid")
```

#### `Worker`

Represents a worker who can be matched to jobs.

**Constructor:**
```python
Worker(name, phone, location, skills, available=True, worker_id=None, registration_date=None)
```

**Methods:**
- `validate()`: Returns `(bool, str)` - (is_valid, error_message)
- `get_skills_list()`: Returns list of skill strings
- `has_skill(skill)`: Returns bool - checks if worker has specific skill
- `to_dict()`: Returns dictionary representation

**Example:**
```python
from models import Worker

worker = Worker(
    name="Jane Smith",
    phone="0987654321",
    location="Kigali, Rwanda",
    skills="Planting, Harvesting"
)

skills = worker.get_skills_list()  # ["Planting", "Harvesting"]
has_skill = worker.has_skill("Planting")  # True
```

#### `Job`

Represents a job posting by a farmer.

**Constructor:**
```python
Job(farmer_id, title, skill_required, location, description=None, 
    duration=None, pay_rate=None, status='open', job_id=None, posted_date=None)
```

**Methods:**
- `validate()`: Returns `(bool, str)` - (is_valid, error_message)
- `to_dict()`: Returns dictionary representation

**Example:**
```python
from models import Job

job = Job(
    farmer_id=1,
    title="Farm Worker Needed",
    skill_required="Planting",
    location="Kigali, Rwanda",
    description="Need experienced worker",
    duration="3 months",
    pay_rate="$500/month"
)

is_valid, error = job.validate()
```

## User Management Module

### `register_farmer()`

Register a new farmer with input prompts.

**Returns:**
- `int` or `None`: Farmer ID if successful, None on failure

**Example:**
```python
import user_management
farmer_id = user_management.register_farmer()
```

### `register_worker()`

Register a new worker with input prompts.

**Returns:**
- `int` or `None`: Worker ID if successful, None on failure

**Example:**
```python
import user_management
worker_id = user_management.register_worker()
```

### `view_farmer_profile(farmer_id)`

Display farmer profile details.

**Parameters:**
- `farmer_id` (int): ID of the farmer

**Example:**
```python
user_management.view_farmer_profile(1)
```

### `view_worker_profile(worker_id)`

Display worker profile details.

**Parameters:**
- `worker_id` (int): ID of the worker

**Example:**
```python
user_management.view_worker_profile(1)
```

### `update_worker_skills(worker_id)`

Update worker skills with input prompt.

**Parameters:**
- `worker_id` (int): ID of the worker

**Example:**
```python
user_management.update_worker_skills(1)
```

### `update_availability(worker_id, available)`

Update worker availability status.

**Parameters:**
- `worker_id` (int): ID of the worker
- `available` (bool): Availability status

**Example:**
```python
user_management.update_availability(1, True)
```

## Job Management Module

### `post_job(farmer_id)`

Post a new job with input prompts.

**Parameters:**
- `farmer_id` (int): ID of the farmer posting the job

**Example:**
```python
import job_management
job_management.post_job(1)
```

### `view_all_jobs()`

Display all available jobs in a formatted table.

**Example:**
```python
job_management.view_all_jobs()
```

### `view_farmer_jobs(farmer_id)`

Display jobs posted by a specific farmer.

**Parameters:**
- `farmer_id` (int): ID of the farmer

**Example:**
```python
job_management.view_farmer_jobs(1)
```

### `search_jobs_by_location(location)`

Search and display jobs by location.

**Parameters:**
- `location` (str): Location to search for

**Example:**
```python
job_management.search_jobs_by_location("Kigali")
```

### `update_job_status(job_id, new_status)`

Update job status (open/filled/closed).

**Parameters:**
- `job_id` (int): ID of the job
- `new_status` (str): New status ('open', 'filled', or 'closed')

**Example:**
```python
job_management.update_job_status(1, "filled")
```

### `delete_job(job_id)`

Delete a job posting.

**Parameters:**
- `job_id` (int): ID of the job to delete

**Example:**
```python
job_management.delete_job(1)
```

## Matching Engine Module

### `match_workers_to_job(job_id, top_n=10)`

Find and rank suitable workers for a job.

**Parameters:**
- `job_id` (int): ID of the job
- `top_n` (int): Number of top matches to return (default: 10)

**Example:**
```python
import matching_engine
matching_engine.match_workers_to_job(1, top_n=5)
```

### `match_jobs_to_worker(worker_id, top_n=10)`

Find and rank suitable jobs for a worker.

**Parameters:**
- `worker_id` (int): ID of the worker
- `top_n` (int): Number of top matches to return (default: 10)

**Example:**
```python
matching_engine.match_jobs_to_worker(1, top_n=5)
```

### `MatchingEngine` Class

Core matching engine class.

**Methods:**
- `match_job_to_workers(job_row, top_n=10)`: Match workers to a job
- `match_worker_to_jobs(worker_row, top_n=10)`: Match jobs to a worker
- `_score_match(...)`: Internal scoring method

**Example:**
```python
from matching_engine import MatchingEngine
import database

engine = MatchingEngine()
job = database.fetch_one("SELECT * FROM jobs WHERE job_id = ?", (1,))
matches = engine.match_job_to_workers(job, top_n=5)
```

### Utility Functions

#### `parse_latlon(location)`

Parse location string as 'lat,lon' coordinates.

**Parameters:**
- `location` (str): Location string in "lat,lon" format

**Returns:**
- `dict` or `None`: Dictionary with 'lat' and 'lon' keys, or None if parsing fails

**Example:**
```python
from matching_engine import parse_latlon
coords = parse_latlon("-1.95,30.06")  # {'lat': -1.95, 'lon': 30.06}
```

#### `match_location_text(loc1, loc2)`

Match two location strings textually.

**Parameters:**
- `loc1` (str): First location string
- `loc2` (str): Second location string

**Returns:**
- `float`: Similarity score between 0.0 and 1.0

**Example:**
```python
from matching_engine import match_location_text
score = match_location_text("Kigali", "Kigali, Rwanda")  # 0.8
```

## Menu Module

### `display_main_menu()`

Show main menu options and get user choice.

**Returns:**
- `int`: User's menu choice (1-7)

**Example:**
```python
from menu import display_main_menu
choice = display_main_menu()
```

### `display_farmer_menu(farmer_name)`

Show farmer-specific menu.

**Parameters:**
- `farmer_name` (str): Name of the farmer

**Returns:**
- `int`: User's menu choice

**Example:**
```python
from menu import display_farmer_menu
choice = display_farmer_menu("John Doe")
```

### `display_worker_menu(worker_name)`

Show worker-specific menu.

**Parameters:**
- `worker_name` (str): Name of the worker

**Returns:**
- `int`: User's menu choice

**Example:**
```python
from menu import display_worker_menu
choice = display_worker_menu("Jane Smith")
```

### `get_user_choice(min_option, max_option)`

Get and validate user menu selection.

**Parameters:**
- `min_option` (int): Minimum valid option number
- `max_option` (int): Maximum valid option number

**Returns:**
- `int`: Valid user choice

**Example:**
```python
from menu import get_user_choice
choice = get_user_choice(1, 7)
```

### `display_job_status_menu()`

Display job status selection menu.

**Returns:**
- `str`: Selected status ('open', 'filled', or 'closed')

**Example:**
```python
from menu import display_job_status_menu
status = display_job_status_menu()
```

### `display_welcome_message()`

Display welcome message on application start.

**Example:**
```python
from menu import display_welcome_message
display_welcome_message()
```

### `display_exit_message()`

Display exit message when application closes.

**Example:**
```python
from menu import display_exit_message
display_exit_message()
```

## Utils Module

### `clear_screen()`

Clear terminal screen.

**Example:**
```python
from utils import clear_screen
clear_screen()
```

### `print_header(title)`

Print formatted header.

**Parameters:**
- `title` (str): Header text

**Example:**
```python
from utils import print_header
print_header("Welcome")
```

### `print_separator()`

Print visual separator line.

**Example:**
```python
from utils import print_separator
print_separator()
```

### `pause()`

Pause and wait for user to press Enter.

**Example:**
```python
from utils import pause
pause()
```

### `print_success(message)`

Print success message.

**Parameters:**
- `message` (str): Success message

**Example:**
```python
from utils import print_success
print_success("Operation completed!")
```

### `print_error(message)`

Print error message.

**Parameters:**
- `message` (str): Error message

**Example:**
```python
from utils import print_error
print_error("Something went wrong!")
```

### `print_info(message)`

Print info message.

**Parameters:**
- `message` (str): Info message

**Example:**
```python
from utils import print_info
print_info("Processing...")
```

### `confirm_action(message)`

Get user confirmation for an action.

**Parameters:**
- `message` (str): Confirmation prompt

**Returns:**
- `bool`: True if confirmed, False otherwise

**Example:**
```python
from utils import confirm_action
if confirm_action("Delete this job?"):
    # Delete job
    pass
```

### `format_table(data, headers)`

Format data as table (legacy function, tabulate is preferred).

**Parameters:**
- `data` (list): List of rows (each row is a list)
- `headers` (list): Column headers

**Returns:**
- `str`: Formatted table string

**Example:**
```python
from utils import format_table
data = [["John", "123"], ["Jane", "456"]]
headers = ["Name", "ID"]
table = format_table(data, headers)
print(table)
```

## Error Handling

All database functions handle errors gracefully:
- Database errors return empty lists or None
- Validation functions return False for invalid input
- User input functions prompt for retry on invalid input

## Best Practices

1. **Always use parameterized queries** to prevent SQL injection
2. **Close database connections** after use
3. **Validate input** before database operations
4. **Handle exceptions** appropriately
5. **Use the database module functions** instead of direct SQLite connections

## Notes

- All database functions use the Row factory for column access by name
- Functions return dictionaries or lists of dictionaries
- The matching engine automatically saves matches to the database
- Location matching supports both text and GPS coordinate formats

