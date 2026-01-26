# FastAPI Todo App - Hugging Face Deployment

This is a production-ready FastAPI backend for the todo application, configured for deployment on Hugging Face Spaces using Docker.

## Architecture
- FastAPI backend with SQLModel and PostgreSQL
- Neon PostgreSQL database integration
- JWT-based authentication
- Docker containerized for Hugging Face Spaces

## Deployment Configuration
- Server: Uvicorn
- Port: Dynamically assigned by Hugging Face ($PORT environment variable)
- Host: 0.0.0.0 (required for Hugging Face)

## Environment Variables Required
- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Docker Configuration
The application is configured to run in a Docker container on Hugging Face Spaces:
- Base image: python:3.10-slim
- System dependencies: gcc, g++
- Python dependencies: As specified in requirements.txt
- Startup command: uvicorn with dynamic port binding

## Endpoints Available
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/auth/signup` - User registration
- `/auth/signin` - User authentication
- `/tasks` - Task management endpoints

## Important Notes
- Due to Hugging Face Spaces ephemeral storage, persistent data relies on external database
- The application is designed to work with Neon PostgreSQL for data persistence
- Authentication tokens are valid for the duration specified in environment variables