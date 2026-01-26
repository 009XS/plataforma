# Utility Scripts

This directory contains helper scripts for the Learning Platform application.

## Available Scripts

### `analyze_backend.py`
Analyzes `app.py` to list all API routes and database tables. Helpful to see what is implemented.
*Usage:* `python scripts/analyze_backend.py`

### `create_test_user.py`
Creates or updates a test admin user (Password: `admin123`).
*Usage:* `python scripts/create_test_user.py`

### `debug_users.py`
Lists all users in the database with their roles and status.
*Usage:* `python scripts/debug_users.py`

## Note
These scripts should be run from the project root directory (one level up) if possible, or they will attempt to locate `app.py` relative to themselves.
