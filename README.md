# Todo App Backend

Backend API for a Todo application built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Create tasks
- Get all tasks
- Update existing tasks
- Delete tasks
- Store data in PostgreSQL

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn
- Docker

## Project Structure

```text
.
|-- app
|   |-- api
|   |   |-- dependencies.py
|   |   `-- routers
|   |       `-- task.py
|   |-- core
|   |   `-- config.py
|   |-- db
|   |   `-- session.py
|   |-- models
|   |   |-- base.py
|   |   `-- task.py
|   |-- repositories
|   |   `-- task.py
|   |-- schemas
|   |   `-- task.py
|   |-- services
|   |   `-- task.py
|   `-- main.py
|-- requirements.txt
`-- README.md
```

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run PostgreSQL with Docker

```bash
docker run --name todo-postgres -e POSTGRES_PASSWORD=admin -p 15432:5432 -d postgres
```

This starts PostgreSQL with:

- user: `postgres`
- password: `admin`
- host: `127.0.0.1`
- port: `15432`
- database: `postgres`

### 4. Configure environment variables

By default, the app uses:

```text
DATABASE_URL=postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres
ALLOWED_ORIGINS=http://localhost:3000
```

You can override them in PowerShell before starting the app:

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
$env:ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### 5. Start the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

- `GET /tasks` returns all tasks
- `POST /tasks` creates a new task
- `PATCH /tasks/{task_id}` updates a task
- `DELETE /tasks/{task_id}` deletes a task

## Route Examples

Base URL:

```text
http://127.0.0.1:8000
```

### 1. Create a task

Request:

```bash
curl -X POST "http://127.0.0.1:8000/tasks" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Buy milk\"}"
```

Request body:

```json
{
  "title": "Buy milk"
}
```

Example response:

```json
{
  "id": "0d8c6e18-7a10-4dc5-b3e3-590188f4d774",
  "title": "Buy milk",
  "completed": false
}
```

### 2. Get all tasks

Request:

```bash
curl "http://127.0.0.1:8000/tasks"
```

Example response:

```json
[
  {
    "id": "0d8c6e18-7a10-4dc5-b3e3-590188f4d774",
    "title": "Buy milk",
    "completed": false
  }
]
```

### 3. Update a task

Replace `{task_id}` with the real task id from the create response.

Request:

```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/0d8c6e18-7a10-4dc5-b3e3-590188f4d774" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Buy milk and bread\",\"completed\":true}"
```

Request body:

```json
{
  "title": "Buy milk and bread",
  "completed": true
}
```

Example response:

```json
{
  "id": "0d8c6e18-7a10-4dc5-b3e3-590188f4d774",
  "title": "Buy milk and bread",
  "completed": true
}
```

### 4. Delete a task

Request:

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/0d8c6e18-7a10-4dc5-b3e3-590188f4d774"
```

Expected result:

- HTTP status: `204 No Content`
- Response body: empty

### Full workflow

1. Send `POST /tasks` to create a new task.
2. Copy the returned `id`.
3. Send `GET /tasks` to confirm the task is stored.
4. Send `PATCH /tasks/{task_id}` to update title or completed status.
5. Send `DELETE /tasks/{task_id}` to remove the task.
6. Send `GET /tasks` again to confirm it is gone.

## Notes

- Tables are currently created on application startup via `Base.metadata.create_all(...)`.
- The project uses a layered structure: router -> service -> repository -> database.
- Migrations are not set up yet. Alembic would be the next reasonable step.
