# Student Registration Portal

Python and SQLite web application for a professional academy with:

- login-first access for all users
- `admin` and `student` roles
- announcements as the post-login landing page
- course management and enrollment approval
- student directory and classmate visibility for approved enrollments
- announcement image uploads

## Stack

- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- SQLite

## Requirements

- Python 3.12 or newer

## How To Run

1. Open a terminal in the project folder:

   ```bash
   cd /workspace/student-registration
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   Linux or macOS:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Seed the database with demo data:

   ```bash
   flask --app app seed
   ```

6. Start the development server:

   ```bash
   flask --app app run --debug
   ```

7. Open the app in your browser:

   ```text
   http://127.0.0.1:5000
   ```

## Demo Accounts

- Admin
  Username: `admin`
  Password: `admin123!`

- Student
  Username: `student1`
  Password: `student123!`

## Project Notes

- SQLite database file: `instance/app.db`
- Announcement uploads: `instance/uploads/announcements/`
- The database is created automatically on first run
- If demo data already exists, the seed command will not create duplicates
- Change `SECRET_KEY` in [config.py](/workspace/student-registration/config.py) before using the app outside local development

## Useful Commands

Create or refresh demo data:

```bash
flask --app app seed
```

Run without activating the virtual environment:

```bash
.venv/bin/flask --app app run --debug
```
