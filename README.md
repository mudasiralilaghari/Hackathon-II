---
title: Full-Stack Todo App
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

# Full-Stack Todo Application

This is a full-stack todo application built with FastAPI (backend) and Next.js (frontend), deployed on Hugging Face Spaces using Docker.

## Features

- User authentication (signup/signin)
- Task management (create, read, update, delete)
- Task completion toggle
- User-specific task isolation
- Persistent storage with Neon PostgreSQL
- JWT-based authentication

## Tech Stack

- Backend: FastAPI
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Authentication: JWT
- Frontend: Next.js (App Router)
- Deployment: Docker on Hugging Face Spaces

## API Endpoints

- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/auth/signup` - Create a new user account
- `/auth/signin` - Authenticate and get JWT token
- `/tasks` - Manage user tasks

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- Backend: FastAPI application with SQLModel ORM, handling authentication and business logic
- Database: Neon PostgreSQL for persistent data storage
- Authentication: JWT-based authentication

## Environment Variables

The application requires the following environment variables to be set in the Space settings:

- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

These have been configured in the Space secrets.