# Reward Platform API

A Django REST Framework based API platform for managing user rewards and scheduled tasks.

## Features

- JWT Authentication
- User profile management
- Reward scheduling system
- Celery task processing
- Swagger/OpenAPI documentation
- Docker support

## Tech Stack

- Django 4.2
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- JWT Authentication
- drf-yasg (Swagger/OpenAPI)

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (if running locally)

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd reward-platform
```

2. Create a `.env` file in the project root with the following variables:
```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Build and start the containers:
```bash
docker-compose up -d --build
```

4. Run migrations:
```bash
docker-compose exec api python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec api python manage.py createsuperuser
```

## API Documentation

Access the Swagger documentation at:
- Swagger UI: http://localhost:8000/swagger/

### Authentication

1. Obtain JWT tokens:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username", "password":"your_password"}'
```

2. Use the access token in subsequent requests:
```bash
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Bearer your_access_token"
```

### API Endpoints

#### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token

#### User Profile
- `GET /api/profile/` - Get user profile (username, email, coins)

#### Rewards
- `GET /api/rewards/` - Get list of user's rewards
- `POST /api/rewards/request/` - Request a new reward (limited to once per day)

## Development

### Running Tests
```bash
docker-compose exec api python manage.py test
```


## Project Structure

```
reward_platform/
├── users/                    # User management app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # Data serializers
│   ├── tasks.py             # Celery tasks
│   └── urls.py              # URL routing
├── reward_platform/         # Project settings
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Service orchestration
└── requirements.txt        # Python dependencies
```

