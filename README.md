# Banking Simulation

## Database Migrations

This project uses Alembic for database migrations.

### Commands

**Create a migration:**
```bash
uv run alembic revision --autogenerate -m "Message"
```

**Apply migrations:**
```bash
uv run alembic upgrade head
```
