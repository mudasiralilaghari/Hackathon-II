# Multi-User Todo Web Application

A full-stack web application that allows users to manage their personal todo lists with secure authentication and data isolation.

## Features

- User authentication (signup/signin)
- Task management (create, read, update, delete)
- Task completion toggle
- User-specific task isolation
- Persistent storage with Neon PostgreSQL
- JWT-based authentication

## Tech Stack

- **Frontend**: Next.js (App Router)
- **Backend**: FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT with Better Auth

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with the following:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
   SECRET_KEY=your-super-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   NEON_DATABASE_URL=your-neon-database-url
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend  # from project root
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env.local` file in the frontend directory with the following:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## API Documentation

The API documentation is available at:
- Backend: `http://localhost:8000/docs` (Swagger UI)
- Backend: `http://localhost:8000/redoc` (ReDoc)

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
- **Authentication**: JWT-based authentication