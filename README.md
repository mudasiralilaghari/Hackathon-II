# Hackathon-2 - Multi-User Todo Full-Stack Web Application

This repository contains the implementation of a multi-user todo web application as part of Hackathon Phase 2.

## Project Overview

The application is a full-stack web application with:
- **Backend**: FastAPI with SQLModel and JWT authentication
- **Frontend**: Next.js with App Router and React components
- **Database**: Neon PostgreSQL with persistent storage
- **Authentication**: Secure JWT-based user authentication with Better Auth
- **Task Management**: Complete CRUD operations with user-specific data isolation

## Features

- User Registration and Authentication (Signup/Signin)
- Task Management (Create, Read, Update, Delete)
- Task Completion Toggle
- User-specific Data Isolation
- Responsive UI Design
- Clean Architecture with Separation of Concerns

## Getting Started

1. Clone the repository
2. Navigate to the `phase-2-todo-fullstack-app` directory
3. Follow the instructions in the README.md file in that directory

## Directory Structure

```
Hackathon-2/
├── phase-1-cli-app/                     # Phase 1 Console Todo App
├── phase-2-todo-fullstack-app/          # Phase 2 Full-Stack Todo Application
│   ├── backend/                         # Backend API (FastAPI)
│   │   ├── src/
│   │   │   ├── api/
│   │   │   ├── middleware/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── .env
│   ├── frontend/                        # Frontend UI (Next.js)
│   │   ├── src/
│   │   │   ├── app/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   └── pages/
│   │   ├── package.json
│   │   └── .env.local
│   ├── specs/                           # Feature specifications
│   ├── history/                         # Development history
│   └── README.md                        # Phase 2 application documentation
├── README.md                            # This file (Project overview)
└── other files...
```

## Phase 2 - Full-Stack Todo Application

The `phase-2-todo-fullstack-app` directory contains the complete implementation of the multi-user todo application with:

- **Backend**: FastAPI with SQLModel and JWT authentication
- **Frontend**: Next.js with App Router and React components
- **Database**: Neon PostgreSQL with persistent storage
- **Authentication**: Secure JWT-based user authentication
- **Task Management**: Complete CRUD operations with user-specific isolation

## Features

- User Registration and Authentication (Signup/Signin)
- Task Management (Create, Read, Update, Delete)
- Task Completion Toggle
- User-specific Data Isolation
- Responsive UI Design
- Clean Architecture with Separation of Concerns

## Getting Started

To run the application:

1. Navigate to the `phase-2-todo-fullstack-app` directory
2. Follow the instructions in the README.md file in that directory

## Access Points

- **Backend API**: http://127.0.0.1:8000
- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://127.0.0.1:8000/docs