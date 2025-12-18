# Django Backend for Smart Placement Portal

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=placement_db
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

## Project Structure

```
backend/
├── placement_portal/      # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── authentication/        # User authentication app
├── students/             # Student management
├── recruiters/           # Recruiter management
├── jobs/                 # Job postings
├── resumes/              # Resume handling
├── ml_integration/       # ML model integration
├── analytics/            # Analytics & reports
└── manage.py
```

## API Endpoints

API documentation will be available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Testing

```bash
python manage.py test
```

## Key Technologies

- **Django 4.2**: Web framework
- **Django REST Framework**: API development
- **Simple JWT**: Token authentication
- **PostgreSQL**: Database
- **PyPDF2**: PDF parsing
- **scikit-learn**: ML algorithms
- **spaCy**: NLP processing
