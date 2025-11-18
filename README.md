# Local Agricultural Job Board & Skills Matcher

A Python CLI application that connects local farmers with agricultural workers through an intelligent job matching system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agri-job-board
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python database.py
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
agri-job-board/
├── main.py                 # Main program entry point
├── database.py             # Database setup and connections
├── models.py               # Data models and validation
├── user_management.py      # User registration and profiles
├── job_management.py       # Job posting and management
├── matching_engine.py      # Job-worker matching algorithm
├── menu.py                 # CLI menu system
├── utils.py                # Utility functions
├── tests/                  # Unit tests
├── data/                   # Database files
└── docs/                   # Documentation
```

## 🛠️ Technology Stack

- **Language:** Python 3.8+
- **Database:** SQLite3
- **Dependencies:** tabulate (for formatted table output)

## 📊 Database Schema

The application uses SQLite with the following tables:
- `farmers` - Farmer registration and profiles
- `workers` - Worker registration and profiles
- `jobs` - Job postings
- `matches` - Job-worker match results

## 👥 Team

- **Modupe Adegoke Akanni** - Database & Models
- **Gavin Ganza** - User Management
- **Sylvie Uwera** - Job Management
- **Divin Semana** - Matching Engine
- **Credo Hedrick Iranzi** - CLI & Main
- **Bruce Eddy Manzi** - Testing & Docs

## 📝 Development

See `docs/` directory for detailed development guide and API documentation.

## 📄 License

This project is part of a team assignment.

