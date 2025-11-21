# User Guide - Local Agricultural Job Board & Skills Matcher

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Farmer Guide](#farmer-guide)
4. [Worker Guide](#worker-guide)
5. [Matching System](#matching-system)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [FAQ](#faq)

## Introduction

The Local Agricultural Job Board & Skills Matcher is a command-line application designed to connect farmers with agricultural workers. Whether you're a farmer looking for skilled workers or a worker seeking job opportunities, this system helps you find the perfect match.

### Key Features

- **Easy Registration**: Quick signup for farmers and workers
- **Job Posting**: Farmers can post detailed job listings
- **Smart Matching**: Automated matching based on skills, location, and availability
- **Profile Management**: Update your information anytime
- **Search Functionality**: Find jobs by location or browse all available positions

## Getting Started

### First Time Setup

1. **Install Python** (3.8 or higher) if you haven't already
2. **Clone or download** the project
3. **Set up virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application**:
   ```bash
   python main.py
   ```

The database will be created automatically on first run - no manual setup required!

## Farmer Guide

### Registering as a Farmer

1. From the main menu, select **"[1] Register as Farmer"**
2. Enter your information:
   - **Full Name**: Your complete name
   - **Phone Number**: Valid phone number (10-15 digits)
   - **Location**: Your location (e.g., "Kigali, Rwanda" or GPS coordinates like "-1.95,30.06")
   - **Email**: Optional email address
3. Your farmer ID will be displayed - save this for reference

### Logging In

1. Select **"[3] Login as Farmer"** from the main menu
2. Choose your profile from the list
3. You'll see the Farmer Dashboard

### Farmer Dashboard Options

#### 1. View My Profile
- See all your registered information
- Check your registration date

#### 2. Post a New Job
- **Title**: Brief job title (e.g., "Farm Worker Needed")
- **Description**: Optional detailed description
- **Required Skill**: The skill needed (e.g., "Planting", "Harvesting", "Irrigation")
- **Location**: Where the job is located
- **Duration**: How long the job lasts (optional)
- **Pay Rate**: Payment information (optional)
- Jobs are automatically set to "open" status

#### 3. View My Posted Jobs
- See all jobs you've posted
- View job status (open/filled/closed)
- Check posting dates

#### 4. Find Workers for a Job
- Select one of your open jobs
- The system will show matching workers ranked by compatibility
- Each match shows:
  - Worker name and skills
  - Match score (0-100%)
  - Location information
  - Matching details

#### 5. Update Job Status
- Change job status to:
  - **Open**: Still accepting applications
  - **Filled**: Position has been filled
  - **Closed**: Job is no longer available

#### 6. Delete a Job
- Permanently remove a job posting
- Requires confirmation

## Worker Guide

### Registering as a Worker

1. From the main menu, select **"[2] Register as Worker"**
2. Enter your information:
   - **Full Name**: Your complete name
   - **Phone Number**: Valid phone number
   - **Location**: Your location
   - **Skills**: Comma-separated list (e.g., "Planting, Harvesting, Irrigation")
   - **Availability**: Are you currently available? (y/n)
3. Your worker ID will be displayed

### Logging In

1. Select **"[4] Login as Worker"** from the main menu
2. Choose your profile from the list
3. You'll see the Worker Dashboard

### Worker Dashboard Options

#### 1. View My Profile
- See all your registered information
- Check your skills and availability status

#### 2. Update My Skills
- Modify your skill list
- Use comma-separated format (e.g., "Planting, Harvesting, Tractor Operation")
- Keep skills current for better job matches

#### 3. Update Availability Status
- Mark yourself as available or not available
- Available workers get priority in matching

#### 4. View All Available Jobs
- Browse all open job postings
- See job details including:
  - Title and description
  - Required skills
  - Location
  - Duration and pay rate
  - Posting date

#### 5. Find Jobs Matching My Skills
- Get personalized job recommendations
- Jobs are ranked by match score
- See why each job matches your profile

#### 6. Search Jobs by Location
- Enter a location to search
- Find jobs in specific areas
- Supports partial matches (e.g., "Kigali" matches "Kigali, Rwanda")

## Matching System

### How Matching Works

The system uses a sophisticated algorithm to match workers with jobs based on three factors:

1. **Skill Match (60% weight)**
   - Compares worker skills with job requirements
   - Exact matches score highest
   - Multiple matching skills increase the score

2. **Location Match (30% weight)**
   - Text-based matching: Compares location strings
   - GPS coordinates: Calculates distance if both have lat/lon format
   - Same location = highest score
   - Partial matches (e.g., both in "Kigali") score well

3. **Availability (10% weight)**
   - Available workers get full points
   - Unavailable workers score lower

### Match Score

Match scores range from 0% to 100%:
- **80-100%**: Excellent match - highly recommended
- **60-79%**: Good match - worth considering
- **40-59%**: Fair match - may require additional skills
- **0-39%**: Poor match - not recommended

### Understanding Match Results

When viewing matches, you'll see:
- **Rank**: Position in the match list
- **Match Score**: Compatibility percentage
- **Details**: Explanation of why it matched (e.g., "skills matched 2/2", "location text match: 0.80")

## Tips and Best Practices

### For Farmers

1. **Be Specific with Skills**: List exact skills needed (e.g., "Tractor Operation" not just "Farming")
2. **Update Job Status**: Mark jobs as "filled" or "closed" when appropriate
3. **Use Clear Locations**: Use consistent location format (e.g., always "City, Country")
4. **Complete Job Details**: Include duration and pay rate for better worker interest
5. **Review Matches**: Check multiple workers, not just the top match

### For Workers

1. **Keep Skills Updated**: Add new skills as you learn them
2. **Be Honest About Availability**: Update your status regularly
3. **Use Specific Skills**: Instead of "Farming", list "Planting, Harvesting, Irrigation"
4. **Location Accuracy**: Use consistent location format
5. **Check Regularly**: New jobs are posted frequently

### Location Formats

The system supports two location formats:

1. **Text Format**: "Kigali, Rwanda", "New York, USA"
   - Case-insensitive
   - Supports partial matching
   - Best for general use

2. **GPS Coordinates**: "-1.95,30.06" (latitude,longitude)
   - Enables distance calculation
   - More precise matching
   - Use if you have exact coordinates

## FAQ

### General Questions

**Q: Do I need to manually create the database?**
A: No! The database is created automatically when you first run the application.

**Q: Can I use the app without internet?**
A: Yes! The application works completely offline. All data is stored locally on your computer.

**Q: How do I backup my data?**
A: Simply copy the `data/agri_jobs.db` file to a safe location.

**Q: Can multiple people use the same database?**
A: The database file can be shared, but only one person should run the application at a time to avoid database locking issues.

### Registration Questions

**Q: What phone number format should I use?**
A: Any format is accepted (with or without dashes, spaces, parentheses). The system validates that it contains 10-15 digits.

**Q: Is email required?**
A: No, email is optional for farmers. Workers don't need email.

**Q: Can I change my information after registration?**
A: Currently, you can update worker skills and availability. Full profile editing may be added in future versions.

### Job Posting Questions

**Q: How many jobs can I post?**
A: There's no limit on the number of jobs you can post.

**Q: Can I edit a job after posting?**
A: You can update the job status, but other details cannot be edited. You may need to delete and repost if major changes are needed.

**Q: What happens to closed jobs?**
A: Closed jobs remain in the database but won't appear in job searches or matching results.

### Matching Questions

**Q: Why didn't I get any matches?**
A: Possible reasons:
- No workers/jobs meet the criteria
- Skills don't match
- Location is too different
- Worker is marked as unavailable

**Q: How often are matches updated?**
A: Matches are calculated in real-time when you request them. They're not pre-calculated.

**Q: Can I see why a match scored a certain way?**
A: Yes! Match results include detailed explanations showing skill matches, location similarity, and availability status.

### Technical Questions

**Q: The app says "Database locked" - what do I do?**
A: Close any other instances of the application. Only one instance should run at a time.

**Q: Can I use a different database?**
A: The database path is configured in `database.py`. Advanced users can modify it, but this is not recommended.

**Q: How do I reset the database?**
A: Delete the `data/agri_jobs.db` file and restart the application. A new database will be created.

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting section](../README.md#-troubleshooting) in the README
2. Review the [API Documentation](API_DOCUMENTATION.md) for technical details
3. Ensure you're using Python 3.8 or higher
4. Verify your virtual environment is activated
5. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Conclusion

The Local Agricultural Job Board & Skills Matcher is designed to be simple and intuitive. Whether you're posting your first job or finding your next opportunity, the system guides you through each step.

Remember:
- Keep your profile updated
- Be specific with skills and locations
- Check matches regularly
- Update job statuses promptly

Happy matching!

