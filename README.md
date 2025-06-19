# Healthcare Backend System

A Django REST Framework (DRF) backend for healthcare management with JWT authentication, patient-doctor relationship management, and PostgreSQL database.

## Features

-  JWT Authentication (Register/Login)
-  Patient Management (CRUD)
-  Doctor Management (CRUD)
-  Patient-Doctor Assignment
-  PostgreSQL Database
-  RESTful API Endpoints
-  Permission-based Access Control

## API Documentation

### Authentication

| Endpoint                | Method | Description                     |
|-------------------------|--------|---------------------------------|
| `/api/auth/register/`   | POST   | Register new user               |
| `/api/auth/login/`      | POST   | Login and get JWT tokens        |
| `/api/auth/token/refresh/` | POST | Refresh access token          |

### Patient Management

| Endpoint                | Method | Description                     |
|-------------------------|--------|---------------------------------|
| `/api/patients/`        | POST   | Create new patient              |
| `/api/patients/`        | GET    | List all patients               |
| `/api/patients/<id>/`   | GET    | Get patient details             |
| `/api/patients/<id>/`   | PUT    | Update patient                  |
| `/api/patients/<id>/`   | DELETE | Delete patient                  |

### Doctor Management

| Endpoint                | Method | Description                     |
|-------------------------|--------|---------------------------------|
| `/api/doctors/`         | POST   | Create new doctor               |
| `/api/doctors/`         | GET    | List all doctors                |
| `/api/doctors/<id>/`    | GET    | Get doctor details              |
| `/api/doctors/<id>/`    | PUT    | Update doctor                   |
| `/api/doctors/<id>/`    | DELETE | Delete doctor                   |

### Patient-Doctor Mapping

| Endpoint                          | Method | Description                     |
|-----------------------------------|--------|---------------------------------|
| `/api/mappings/`                  | POST   | Assign doctor to patient        |
| `/api/mappings/`                  | GET    | List all mappings               |
| `/api/mappings/<id>/`             | GET    | Get mapping details             |
| `/api/mappings/<id>/`             | DELETE | Remove doctor from patient      |
| `/api/mappings/patient/<patient_id>/` | GET | Get all doctors for a patient |

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/healthcare-backend.git
   cd healthcare-backend
   ```

### Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Create .env file:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### Run migrations:

```bash
python manage.py migrate
```

### Create superuser:

```bash
python manage.py createsuperuser
```

### Run development server:

```bash
python manage.py runserver
```

### Register a user:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "confirm_password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}'
```

### Login to get tokens:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "password": "testpass123"
}'
```

### Access protected endpoint (use the access token):

```bash
curl -X GET http://127.0.0.1:8000/api/patients/ \
-H "Authorization: Bearer your.access.token.here"
```

### Project Structure

```bash
healthcare-backend/
├── healthcare/
│   ├── models.py         # Database models
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # API endpoints
│   └── admin.py          # Admin panel config
├── healthcare_backend/
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL router
├── .env                  # Environment variables
└── manage.py             # Django management
```
