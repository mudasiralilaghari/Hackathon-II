# Data Model: Multi-User Todo Web Application

## Entities

### User
**Description**: Represents a registered user with unique account credentials

**Fields**:
- `id` (UUID/Integer): Unique identifier for the user (Primary Key)
- `email` (String): User's email address (Unique, Required, Validated)
- `username` (String): User's chosen username (Unique, Required, 3-30 chars)
- `password_hash` (String): Hashed password (Required, Securely stored)
- `created_at` (DateTime): Account creation timestamp (Auto-generated)
- `updated_at` (DateTime): Last update timestamp (Auto-generated)
- `is_active` (Boolean): Account status (Default: true)

**Validation Rules**:
- Email must be a valid email format
- Username must be 3-30 characters, alphanumeric with underscores/hyphens
- Password must meet security requirements (handled by auth library)
- Email and username must be unique across all users

**Relationships**:
- One-to-Many: User has many Tasks

### Task
**Description**: Represents a todo item with title, description, completion status, creation date, and association to a specific user

**Fields**:
- `id` (UUID/Integer): Unique identifier for the task (Primary Key)
- `title` (String): Task title (Required, Max 200 chars)
- `description` (Text): Optional task description (Max 1000 chars)
- `is_completed` (Boolean): Completion status (Default: false)
- `created_at` (DateTime): Task creation timestamp (Auto-generated)
- `updated_at` (DateTime): Last update timestamp (Auto-generated)
- `user_id` (UUID/Integer): Foreign key linking to User (Required)

**Validation Rules**:
- Title must not be empty
- Title must be between 1-200 characters
- Description (if provided) must be under 1000 characters
- user_id must reference an existing, active user

**Relationships**:
- Many-to-One: Task belongs to one User
- User has many Tasks

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user toggles task completion status
- **Complete → Incomplete**: When user toggles task completion status back

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

## Constraints

### Data Integrity
- Foreign key constraint ensures tasks are linked to valid users
- Cascade delete ensures tasks are removed when a user is deleted
- Unique constraints on email and username for users
- Required field constraints to prevent null values where inappropriate

### Access Control
- All queries must filter by user_id to ensure user-specific data isolation
- No cross-user data access is permitted