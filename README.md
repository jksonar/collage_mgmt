# College Management System

A comprehensive Django-based College Management System that handles various aspects of college administration.

## Features

- Student Management
- Course Management
- Faculty Management
- Attendance System
- Grade Management
- Department Management

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `college_mtmt/` - Main project directory
- `apps/` - Django applications
  - `students/` - Student management
  - `courses/` - Course management
  - `faculty/` - Faculty management
  - `attendance/` - Attendance system
  - `grades/` - Grade management
  - `departments/` - Department management 