# JobTracker — Django REST API

A production-ready REST API for tracking job applications.
Built with Django, Django REST Framework, PostgreSQL, and JWT Authentication.

## Features
- JWT Authentication (Login, Register, Token Refresh)
- Full CRUD for Job Applications
- Owner-based filtering — each user sees only their data
- Search, Filtering, and Ordering
- Custom Permissions — only owner can edit/delete
- Throttling — rate limiting
- Statistics endpoint
- Django Templates UI (Login, Dashboard, Forms)
- PostgreSQL database

## Tech Stack
- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL
- JWT (djangorestframework-simplejwt)
- django-filter

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/jobtracker.git
cd jobtracker

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create .env file
DB_NAME=jobtracker
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key

### 5. Run migrations
python manage.py migrate

### 6. Create superuser
python manage.py createsuperuser

### 7. Run server
python manage.py runserver

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/token/ | Get JWT token |
| POST | /api/token/refresh/ | Refresh token |
| GET | /api/jobs/ | List all jobs |
| POST | /api/jobs/ | Create job |
| GET | /api/jobs/{id}/ | Get single job |
| PUT | /api/jobs/{id}/ | Update job |
| PATCH | /api/jobs/{id}/ | Partial update |
| DELETE | /api/jobs/{id}/ | Delete job |
| GET | /api/jobs/statistics/ | Get statistics |

## UI Pages
| URL | Description |
|-----|-------------|
| /accounts/login/ | Login page |
| /register/ | Register page |
| /dashboard/ | Job applications dashboard |
| /jobs/create/ | Add new application |
| /admin/ | Django admin panel |
