# Local Agricultural Job Board & Skills Matcher

A Python CLI application that connects local farmers with agricultural workers through an intelligent job matching system. This application helps farmers find qualified workers and enables workers to discover job opportunities based on skills and location matching.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Technology Stack](#-technology-stack)
- [Development](#-development)
- [Testing](#-testing)
- [Team](#-team)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Features

- **User Registration**: Register as a farmer or worker with profile management
- **Job Posting**: Farmers can post jobs with detailed requirements
- **Job Search**: Search jobs by location, skills, or status
- **Intelligent Matching**: Advanced algorithm matches workers to jobs based on:
  - Skill compatibility (60% weight)
  - Location proximity (30% weight)
  - Worker availability (10% weight)
- **Profile Management**: Update skills, availability, and job statuses
- **Match History**: Track and view previous job-worker matches

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager (usually comes with Python)
- **Operating System**: Windows, macOS, or Linux

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd agriculture-job-board
```

### Step 2: Create Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `tabulate==0.9.0` - For formatted table output

### Step 4: Run the Application

```bash
python main.py
```

**Note**: The database will be automatically created on first run at `data/agri_jobs.db`. The `data/` directory will be created automatically if it doesn't exist. You don't need to manually initialize the database.

## 📖 Usage

### Main Menu Options

When you start the application, you'll see the main menu:

```
[1] Register as Farmer
[2] Register as Worker
[3] Login as Farmer
[4] Login as Worker
[5] View Available Jobs
[6] Search Jobs by Location
[7] Exit
```

### Farmer Workflow

1. **Register**: Choose option 1 to register as a farmer
2. **Login**: Choose option 3 and select your farmer profile
3. **Post Jobs**: From the farmer menu, post new job opportunities
4. **Find Workers**: Use the matching system to find suitable workers for your jobs
5. **Manage Jobs**: Update job status or delete jobs as needed

### Worker Workflow

1. **Register**: Choose option 2 to register as a worker
2. **Login**: Choose option 4 and select your worker profile
3. **Update Profile**: Keep your skills and availability status up to date
4. **Find Jobs**: Use the matching system to discover jobs matching your skills
5. **Search**: Browse available jobs or search by location

### Matching System

The matching algorithm calculates compatibility scores (0-100%) based on:

- **Skills Match (60%)**: How well the worker's skills match job requirements
- **Location Match (30%)**: Proximity between worker and job location
  - Supports both text-based location matching and GPS coordinates (lat/lon)
- **Availability (10%)**: Whether the worker is marked as available

## 📁 Project Structure

```
agriculture-job-board/
├── main.py                 # Main program entry point
├── database.py             # Database setup and connection management
├── models.py               # Data models and validation functions
├── user_management.py      # User registration and profile management
├── job_management.py       # Job posting and management operations
├── matching_engine.py      # Job-worker matching algorithm
├── menu.py                 # CLI menu system and navigation
├── utils.py                # Utility functions (screen clearing, formatting)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
│
├── data/                  # Database files (auto-generated, not in git)
│   └── agri_jobs.db       # SQLite database
│
├── tests/                 # Unit tests
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_user_management.py
│   ├── test_job_management.py
│   └── test_matching_engine.py
│
└── docs/                  # Documentation
    ├── USER_GUIDE.md      # User manual
    ├── API_DOCUMENTATION.md # API reference
    └── DEVELOPMENT.md     # Development guide
```

## 📊 Database Schema

The application uses SQLite with the following tables:

### `farmers` Table
- `farmer_id` (INTEGER, PRIMARY KEY)
- `name` (TEXT, NOT NULL)
- `phone` (TEXT, NOT NULL)
- `location` (TEXT, NOT NULL)
- `email` (TEXT, optional)
- `registration_date` (TIMESTAMP, auto-generated)

### `workers` Table
- `worker_id` (INTEGER, PRIMARY KEY)
- `name` (TEXT, NOT NULL)
- `phone` (TEXT, NOT NULL)
- `location` (TEXT, NOT NULL)
- `skills` (TEXT, NOT NULL) - Comma-separated skills
- `available` (BOOLEAN, DEFAULT 1)
- `registration_date` (TIMESTAMP, auto-generated)

### `jobs` Table
- `job_id` (INTEGER, PRIMARY KEY)
- `farmer_id` (INTEGER, FOREIGN KEY → farmers)
- `title` (TEXT, NOT NULL)
- `description` (TEXT, optional)
- `skill_required` (TEXT, NOT NULL)
- `location` (TEXT, NOT NULL)
- `duration` (TEXT, optional)
- `pay_rate` (TEXT, optional)
- `status` (TEXT, DEFAULT 'open') - 'open', 'filled', or 'closed'
- `posted_date` (TIMESTAMP, auto-generated)

### `matches` Table
- `match_id` (INTEGER, PRIMARY KEY)
- `job_id` (INTEGER, FOREIGN KEY → jobs)
- `worker_id` (INTEGER, FOREIGN KEY → workers)
- `match_score` (INTEGER) - Compatibility score (0-100)
- `match_date` (TIMESTAMP, auto-generated)

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Database**: SQLite3 (file-based, no server required)
- **Dependencies**: 
  - `tabulate==0.9.0` - Table formatting
- **Standard Library**: sqlite3, os, datetime, re

## 💻 Development

### Running Tests

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_database.py

# Run with verbose output
python -m pytest tests/ -v
```

### Code Style

- **Functions**: `snake_case` (e.g., `register_farmer()`)
- **Classes**: `PascalCase` (e.g., `class Farmer`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DB_PATH`)
- **Variables**: `snake_case` (e.g., `farmer_id`)

### Adding New Features

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Update documentation
5. Submit a pull request

## 🧪 Testing

The project includes comprehensive unit tests. See the `tests/` directory for test files covering:

- Database operations
- Data models and validation
- User management functions
- Job management functions
- Matching algorithm

Run tests with:
```bash
python -m pytest tests/ -v
```

## 👥 Team

| Name | Module | Responsibility |
|------|--------|----------------|
| **Modupe Adegoke Akanni** | Database & Models | Database schema, data validation |
| **Gavin Ganza** | User Management | User registration and profiles |
| **Sylvie Uwera** | Job Management | Job posting and management |
| **Divin Semana** | Matching Engine | Matching algorithm and scoring |
| **Credo Hedrick Iranzi** | CLI & Main | Menu system and application flow |
| **Bruce Eddy Manzi** | Testing & Docs | Unit tests and documentation |

## 🐛 Troubleshooting

### Database Issues

**Problem**: "Database locked" error
- **Solution**: Ensure only one instance of the application is running. Close any other instances.

**Problem**: Database file not found
- **Solution**: The database is created automatically on first run. If issues persist, delete the `data/` folder and restart the app.

### Import Errors

**Problem**: "No module named 'tabulate'"
- **Solution**: Make sure you've activated the virtual environment and installed dependencies:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Problem**: "No module named 'database'"
- **Solution**: Ensure you're running the application from the project root directory.

### Location Matching

**Problem**: Location matching not working
- **Solution**: The system supports both text-based locations (e.g., "Kigali, Rwanda") and GPS coordinates (e.g., "-1.95,30.06"). Text matching is case-insensitive and supports partial matches.

### General Issues

**Problem**: Application crashes on startup
- **Solution**: 
  1. Check Python version: `python3 --version` (should be 3.8+)
  2. Verify virtual environment is activated
  3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📝 Notes

- The database file (`data/agri_jobs.db`) is not tracked in git (see `.gitignore`)
- The database is automatically created on first application run
- All data is stored locally in SQLite format
- The application uses `CREATE TABLE IF NOT EXISTS`, so it's safe to run multiple times

## 📄 License

This project is part of a team assignment.

## 📚 Additional Documentation

For more detailed information, see:
- [User Guide](docs/USER_GUIDE.md) - Complete user manual
- [API Documentation](docs/API_DOCUMENTATION.md) - Function reference
- [Development Guide](docs/DEVELOPMENT.md) - Development setup and guidelines
