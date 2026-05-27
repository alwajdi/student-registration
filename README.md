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
   http://127.0.0.1:5000/demo
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
- The app is configured to run under the `/demo` URL prefix
- Change `SECRET_KEY` in [config.py](/workspace/student-registration/config.py) before using the app outside local development

## Deploying Under `/demo`

The app now supports the `/demo` base path in two ways:

- direct local access at `http://127.0.0.1:5000/demo`
- reverse-proxy deployments that forward `X-Forwarded-Prefix: /demo`

### Nginx example

```nginx
location /demo/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Prefix /demo;
}
```

### Apache note

Mount the WSGI app at `/demo` and preserve the forwarded host and prefix so
Flask generates links correctly.

## Useful Commands

Create or refresh demo data:

```bash
flask --app app seed
```

Run without activating the virtual environment:

```bash
.venv/bin/flask --app app run --debug
```
