# Developer Documentation

## Ruff

Ruff is used for linting and formatting the Python codebase.

### Commands

```bash
# Check code for lint issues
ruff check

# Check and automatically fix issues
ruff check --fix

# Format the code
ruff format
```

---

## Alembic

Alembic is used for database migrations.

### Commands

```bash
# Apply all migrations up to the latest (head)

alembic upgrade head

# Create a new revision based on model changes
autogenerate
alembic revision --autogenerate -m "migration message"
```

> **Note:** Each developer runs migrations locally, so the database schema will be the same after running `alembic upgrade head`, but the data (records) will not be shared.

---

## FastAPI / Uvicorn

Used to run the API server locally.

### Commands

```bash
# Start the server with auto-reload
uvicorn app.main:app --reload
```

After starting the server, you can access the interactive documentation at:

```
http://127.0.0.1:8000/docs
```

---

## .env configuration

The project expects a `.env` file at the root of the repository with the database connection string.

### Example

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/database_name
```

Make sure this file is **not** committed to the repository and is included in `.gitignore`.
