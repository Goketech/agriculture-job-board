# Development Guide - Local Agricultural Job Board & Skills Matcher

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Database Design](#database-design)
5. [Module Responsibilities](#module-responsibilities)
6. [Testing Guidelines](#testing-guidelines)
7. [Git Workflow](#git-workflow)
8. [Common Tasks](#common-tasks)
9. [Debugging Tips](#debugging-tips)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agriculture-job-board
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies** (optional, for testing)
   ```bash
   pip install pytest pytest-cov
   ```

5. **Run tests** to verify setup
   ```bash
   python -m pytest tests/ -v
   ```

## Project Structure

```
agriculture-job-board/
├── main.py                 # Application entry point
├── database.py             # Database operations
├── models.py               # Data models and validation
├── user_management.py       # User registration and profiles
├── job_management.py       # Job posting and management
├── matching_engine.py       # Matching algorithm
├── menu.py                 # CLI menu system
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
├── README.md               # Main documentation
├── .gitignore             # Git ignore rules
│
├── data/                   # Database files (auto-generated)
│   └── agri_jobs.db
│
├── tests/                  # Unit tests
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_user_management.py
│   ├── test_job_management.py
│   └── test_matching_engine.py
│
└── docs/                   # Documentation
    ├── USER_GUIDE.md
    ├── API_DOCUMENTATION.md
    └── DEVELOPMENT.md
```

## Code Style Guidelines

### Naming Conventions

- **Functions**: `snake_case` (e.g., `register_farmer()`)
- **Classes**: `PascalCase` (e.g., `class Farmer`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DB_PATH`)
- **Variables**: `snake_case` (e.g., `farmer_id`)
- **Private methods**: Prefix with underscore (e.g., `_score_match()`)

### Function Documentation

All functions should have docstrings:

```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Code Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate logical sections
- Import statements at the top, grouped:
  1. Standard library
  2. Third-party packages
  3. Local modules

### Error Handling

Always handle errors appropriately:

```python
try:
    result = database.execute_query(query, params)
except sqlite3.Error as e:
    print_error(f"Database error: {e}")
    return None
except Exception as e:
    print_error(f"Unexpected error: {e}")
    return None
```

## Database Design

### Schema Overview

The database uses SQLite with four main tables:

1. **farmers**: Farmer registration and profiles
2. **workers**: Worker registration and profiles
3. **jobs**: Job postings
4. **matches**: Job-worker match results

### Database Access Pattern

Always use the `database.py` module functions:

```python
# Good
result = database.fetch_one("SELECT * FROM farmers WHERE farmer_id = ?", (id,))

# Bad - Direct connection
conn = sqlite3.connect("data/agri_jobs.db")
```

### Connection Management

- Use `database.get_connection()` for manual operations
- Always close connections: `conn.close()`
- Use `database.execute_query()` for write operations
- Use `database.fetch_one()` or `database.fetch_all()` for read operations

## Module Responsibilities

### `main.py`
- Application entry point
- Main program loop
- Route user choices to appropriate functions
- Handle system initialization

### `database.py`
- Database initialization
- Connection management
- Query execution
- Data fetching

### `models.py`
- Data validation functions
- Model classes (Farmer, Worker, Job)
- Input validation logic

### `user_management.py`
- User registration
- Profile viewing and updating
- User data management

### `job_management.py`
- Job posting
- Job viewing and searching
- Job status management
- Job deletion

### `matching_engine.py`
- Matching algorithm implementation
- Score calculation
- Match display
- Location matching logic

### `menu.py`
- Menu display functions
- User input handling
- Navigation logic

### `utils.py`
- Screen management
- Formatting utilities
- User interaction helpers

## Testing Guidelines

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_database.py

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

1. **Use unittest.TestCase** for test classes
2. **Set up test fixtures** in `setUp()` method
3. **Clean up** in `tearDown()` method
4. **Use descriptive test names**: `test_function_name_scenario()`
5. **Test edge cases**: empty inputs, None values, invalid data
6. **Use temporary databases** for database tests

### Test Structure

```python
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import module_to_test

class TestModule(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_function_name_scenario(self):
        """Test description."""
        # Arrange
        # Act
        # Assert
        pass
```

## Git Workflow

### Branch Strategy

```
main (production-ready code)
├── dev (integration branch)
    ├── feature/database
    ├── feature/user-management
    ├── feature/job-management
    ├── feature/matching
    ├── feature/cli-menu
    └── feature/testing
```

### Commit Message Format

```
[Module] Brief description

Examples:
[Database] Add farmers table creation
[UserMgmt] Implement farmer registration
[JobMgmt] Add job search by location
[Matching] Implement scoring algorithm
[CLI] Add main menu display
[Tests] Add user registration tests
```

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No linter errors
- [ ] Code reviewed

## Common Tasks

### Adding a New Feature

1. Create a feature branch
   ```bash
   git checkout -b feature/new-feature
   ```

2. Implement the feature
   - Write code following style guidelines
   - Add docstrings
   - Handle errors appropriately

3. Write tests
   - Add test cases for new functionality
   - Test edge cases

4. Update documentation
   - Update README if needed
   - Update API documentation
   - Update user guide if user-facing

5. Commit and push
   ```bash
   git add .
   git commit -m "[Module] Add new feature"
   git push origin feature/new-feature
   ```

6. Create pull request

### Fixing a Bug

1. Create a bugfix branch
   ```bash
   git checkout -b bugfix/description
   ```

2. Reproduce the bug
   - Write a test that fails
   - Document the issue

3. Fix the bug
   - Implement the fix
   - Ensure test passes

4. Test thoroughly
   - Run all tests
   - Test edge cases

5. Commit and push
   ```bash
   git commit -m "[Module] Fix bug description"
   ```

### Refactoring Code

1. Ensure tests exist
2. Run tests to verify current behavior
3. Refactor code
4. Run tests again to ensure nothing broke
5. Update documentation if needed

## Debugging Tips

### Database Issues

**Problem**: Database locked
- **Solution**: Ensure only one connection/instance is open
- **Check**: Look for unclosed connections

**Problem**: Data not persisting
- **Solution**: Ensure `conn.commit()` is called after writes
- **Check**: Verify transaction handling

### Import Errors

**Problem**: "No module named 'X'"
- **Solution**: Check PYTHONPATH, ensure running from project root
- **Check**: Verify virtual environment is activated

### Matching Algorithm Issues

**Problem**: Unexpected match scores
- **Solution**: Check location format (text vs GPS)
- **Check**: Verify skill matching logic
- **Debug**: Add print statements to see intermediate scores

### Testing Issues

**Problem**: Tests fail with database errors
- **Solution**: Ensure tests use temporary databases
- **Check**: Verify `setUp()` and `tearDown()` methods

### General Debugging

1. **Use print statements** for quick debugging
2. **Check error messages** carefully
3. **Verify input data** at each step
4. **Test functions in isolation**
5. **Use Python debugger** (`pdb`) for complex issues

```python
import pdb; pdb.set_trace()  # Set breakpoint
```

## Performance Considerations

- **Database queries**: Use indexes for frequently queried columns
- **Matching algorithm**: Limit results with `top_n` parameter
- **Connection pooling**: Not needed for SQLite, but good practice for future SQL migration

## Security Considerations

- **SQL Injection**: Always use parameterized queries
- **Input Validation**: Validate all user input
- **Error Messages**: Don't expose sensitive information in error messages
- **File Permissions**: Ensure database file has appropriate permissions

## Future Enhancements

Potential improvements for future versions:

1. **Authentication**: Add password-based login
2. **Data Export**: Export data to CSV/JSON
3. **Advanced Search**: Filter by multiple criteria
4. **Notifications**: Email/SMS notifications for matches
5. **Web Interface**: Convert CLI to web application
6. **API**: RESTful API for programmatic access
7. **Analytics**: Dashboard with statistics
8. **Multi-language**: Support for multiple languages

## Resources

- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Tabulate Library](https://pypi.org/project/tabulate/)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.html)
- [PEP 8 Style Guide](https://pep8.org/)

## Getting Help

- Review existing code for examples
- Check test files for usage patterns
- Consult API documentation
- Ask team members for guidance

Happy coding!

