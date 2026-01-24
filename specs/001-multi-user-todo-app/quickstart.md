# Quickstart Guide: Multi-User Todo Web Application

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (or access to Neon PostgreSQL)
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Navigate to the backend directory:
```bash
cd backend
```

#### Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Set up environment variables:
Create a `.env` file in the backend directory with the following:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

#### Run database migrations:
```bash
alembic upgrade head
```

#### Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to the frontend directory:
```bash
cd frontend  # from project root
```

#### Install dependencies:
```bash
npm install
```

#### Set up environment variables:
Create a `.env.local` file in the frontend directory with the following:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
```

#### Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Documentation

The API documentation is available at:
- Backend: `http://localhost:8000/docs` (Swagger UI)
- Backend: `http://localhost:8000/redoc` (ReDoc)

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Key Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/signin` - Authenticate and get JWT token

### Tasks
- `GET /tasks` - Get all tasks for the authenticated user
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/toggle` - Toggle task completion status

## Architecture Overview

The application follows a clean architecture pattern with clear separation of concerns:

- **Backend**: FastAPI application with SQLModel ORM, handling authentication and business logic
- **Frontend**: Next.js application with React components, handling user interface and interactions
- **Database**: Neon PostgreSQL for persistent data storage
- **Authentication**: JWT-based authentication with Better Auth