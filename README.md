# Todo App Backend

A simple backend API for a Todo application built with `FastAPI` and `PostgreSQL`.

This project was created as a practice backend application and includes a Docker-based PostgreSQL setup, database persistence, and basic CRUD operations for tasks.

## Features

- Create tasks
- Get all tasks
- Update existing tasks
- Delete tasks
- Store data in PostgreSQL instead of in-memory storage

## Tech Stack

- `Python 3.13`
- `FastAPI`
- `SQLAlchemy`
- `PostgreSQL`
- `Docker`
- `Uvicorn`

## Project Structure

```text
.
├── main.py
├── requerements.txt
└── README.md
```

## Getting Started

### 1. Run PostgreSQL with Docker

```bash
docker run --name my-container -e POSTGRES_PASSWORD=admin -p 15432:5432 -d postgres
```

This command starts a PostgreSQL container with:

- database user: `postgres`
- password: `admin`
- local port: `15432`

### 2. Install dependencies

```bash
pip install -r requerements.txt
```

If needed, install the database packages manually:

```bash
pip install sqlalchemy psycopg[binary]
```

### 3. Start the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## Database Configuration

The current connection string used in the project:

```python
postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres
```

## API Endpoints

- `GET /tasks` — return all tasks
- `POST /tasks` — create a new task
- `PATCH /tasks/{task_id}` — update a task
- `DELETE /tasks/{task_id}` — delete a task

### Example: Create a task

```json
{
  "title": "Buy milk"
}
```

### Example: Update a task

```json
{
  "title": "Buy milk and bread",
  "completed": true
}
```

## Development Notes

This project is still in progress and can be improved further by:

- moving database settings into environment variables
- adding migrations with `Alembic`
- renaming `requerements.txt` to `requirements.txt`
- splitting the application into separate modules
- adding tests and better validation

## Purpose

This repository is part of my backend learning practice and demonstrates:

- working with REST APIs in FastAPI
- connecting a Python app to PostgreSQL
- running services with Docker
- implementing basic database CRUD operations
