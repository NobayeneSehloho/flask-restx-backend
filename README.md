# Flask-RESTX Backend

RESTful API built with Flask-RESTX, SQLAlchemy, and SQLite.

## Features

- RESTful API with Swagger documentation
- SQLAlchemy ORM with SQLite database
- CORS enabled for frontend communication
- Automatic database initialization
- Health check endpoint
- JWT authentication support

## Requirements (check the requirements.txt file for complete list)

- Python 3.12+
- Flask 3.1.3
- Flask-RESTX 1.3.2
- Flask-SQLAlchemy 3.0.3
- Flask-CORS 6.0.0

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
flask run
```

The API will be available at http://localhost:5000

## Docker

### Build Image (or can use your own chosen version numbers)

```bash
docker build -t flask-restx-backend:v1.0.1 .
```

### Run Container

```bash
docker run -d -p 5000:5000 flask-restx-backend:v1.0.1
```

### With Docker Network

```bash
docker network create flask-restx-network
docker run -d --name flask-restx-backend \
  --network flask-restx-network \
  -p 5000:5000 \
  flask-restx-backend:v1.0.1
```

## API Endpoints

### Courses

- `GET /api/courses` - List all courses
- `POST /api/courses` - Create a course
  ```json
  {"name": "Computer Science"}
  ```
- `GET /api/courses/{id}` - Get course by ID
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

### Students

- `GET /api/students` - List all students
- `POST /api/students` - Create a student
  ```json
  {"name": "John Doe", "course_id": 1}
  ```
- `GET /api/students/{id}` - Get student by ID
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Health

- `GET /health` - Health check endpoint
  ```json
  {"status": "healthy"}
  ```

## API Documentation

Interactive Swagger UI available at http://localhost:5000

## Database

- SQLite database (auto-created on startup)
- Tables: `course`, `student`
- Location: `/app/instance/db.sqlite3` (in container)

## Environment Variables

- `DATABASE_URL` - Database connection string (default: `sqlite:///db.sqlite3`)
- `FLASK_APP` - Flask application module (default: `app`)
- `FLASK_DEBUG` - Debug mode (default: `True`)

## Health Check

The Docker image includes a health check that runs every 30 seconds:
```bash
curl -f http://localhost:5000/health || exit 1
```

## Security

- All dependencies scanned with Trivy (0 vulnerabilities)
- Flask-CORS 6.0.0 (latest secure version)
- Updated typing_extensions for Python 3.12 compatibility

## Project Structure

```
flask-restx-backend/
├── app/
│   ├── __init__.py       # App factory
│   ├── models.py         # Database models
│   ├── resources.py      # API endpoints
│   ├── api_models.py     # API schemas
│   ├── extensions.py     # Extensions (db, api)
│   └── auth.py          # Authentication
├── Dockerfile
├── requirements.txt
└── .flaskenv
```

## Notes

- Database is non-persistent in Docker (recreated on container restart)
- For production, use PostgreSQL or MySQL with persistent storage
- CORS is configured to allow all origins (adjust for production)
