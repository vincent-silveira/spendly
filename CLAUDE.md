# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — A Flask-based expense tracker web application. Currently in early development with implemented landing, authentication, and legal pages. Core expense tracking features (add/edit/delete expenses, user profile, logout) are placeholder routes awaiting implementation.

**Stack:** Python 3, Flask 3.1.3, Jinja2 templates, SQLite (via `database/db.py`), pytest for testing.

## Setup Commands (Step by Step)

```bash
# 1. Clone and enter the repository
cd expense-tracker

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database (once db.py is implemented)
# python -c "from database.db import init_db; init_db()"

# 5. Run development server
python app.py
# Server runs at http://localhost:5001
```

## Development Commands

| Task | Command |
|------|---------|
| Run development server | `python app.py` |
| Run tests | `pytest` |
| Run tests with coverage | `pytest --cov` |
| Run single test file | `pytest test_filename.py` |
| Run tests in watch mode | `pytest --watch` |

## Project Structure (General)

```
expense-tracker/
├── app.py                 # Main Flask app, route definitions
├── requirements.txt       # Python dependencies
├── database/              # Data layer package
│   ├── __init__.py
│   └── db.py              # Database connection, schema, seed functions
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Master layout (navbar, footer, modal)
│   ├── landing.html       # Marketing landing page
│   ├── *.html             # Auth pages, legal pages, future feature pages
├── static/                # Frontend assets
│   ├── css/style.css      # Complete styling with CSS custom properties
│   └── js/main.js         # Client-side JavaScript
└── venv/                  # Virtual environment (gitignored)
```

## Architecture Notes

### Routing (app.py)
- **Implemented:** `/` (landing), `/register`, `/login`, `/terms`, `/policy`
- **Placeholders** (return plain text): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`
- Server runs on **port 5001** with debug mode enabled

### Database Layer (database/db.py)
Currently a stub. Expected to implement:
- `get_db()` — Returns SQLite connection with `row_factory=sqlite3.Row` and foreign keys enabled
- `init_db()` — Creates tables with `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — Inserts sample data for development

### Templates
All pages extend `base.html` which provides:
- Sticky navbar with brand, auth links
- Footer with brand, tagline, Terms/Privacy links
- YouTube video modal (triggered from landing page)
- CSS/JS asset inclusion via `url_for('static', ...)`

### Styling (static/css/style.css)
- CSS custom properties for theming (`--ink`, `--paper`, `--accent`, `--accent-2`, `--danger`, `--border`)
- Fonts: `DM Serif Display` (display), `DM Sans` (body) — loaded via Google Fonts
- Responsive breakpoints: 900px, 600px
- Component classes: `.btn-primary`, `.btn-ghost`, `.form-input`, `.auth-card`, `.feature-card`, `.stat-card`, `.modal-overlay`

## Code Style

- **Python:** Follow PEP 8, use type hints where practical
- **Flask:** Blueprints not yet used; routes defined directly in `app.py`
- **Templates:** Jinja2 inheritance (`{% extends "base.html" %}`), block-based overrides
- **CSS:** BEM-inspired class naming, custom properties for all colors/spacing
- **JavaScript:** Vanilla ES6+, event delegation, no frameworks
- **Database:** Parameterized queries only — never string interpolation

## Tech Constraints

- **Python 3.10+** required (Flask 3.x compatibility)
- **SQLite** for development; no migrations system yet
- **No ORM** — raw SQL in `database/db.py`
- **No authentication library** — custom implementation expected
- **Single-process dev server** — not suitable for production
- **Port 5001** hardcoded in `app.py` (change if conflicts)

## Testing

- Framework: `pytest` with `pytest-flask` plugin
- Test files: `test_*.py` naming convention
- Flask test client via `pytest-flask` fixtures (`client`, `app`)
- Run `pytest` from project root

## Git & Environment

- `.gitignore` excludes: `venv/`, `expense_tracker.db`, `__pycache__/`, `*.pyc`, `.env`, `.DS_Store`, `.claude/plans/`
- Virtual environment in `venv/` (create locally)
- No required environment variables for basic development
- Main branch: `master`

## Warnings & Things to Avoid

| Issue | Avoid |
|-------|-------|
| **SQL Injection** | Never use f-strings or `%` formatting in SQL — always use `?` placeholders |
| **Secret Leakage** | Never commit `.env`, API keys, or `expense_tracker.db` with real data |
| **Template XSS** | Escape user input with `{{ ... }}` (auto-escaped); use `\|safe` only when certain |
| **Debug Mode** | Don't enable `debug=True` in production — exposes stack traces |
| **DB Connections** | Don't open connections globally — use `get_db()` per request |
| **Static Files** | Don't hardcode `/static/...` — always use `url_for('static', filename=...)` |
| **Port Conflicts** | Port 5001 may conflict with AirPlay on macOS — change in `app.py` if needed |
| **Circular Imports** | Import `db` functions inside route functions, not at module level in `app.py` |
| **Global State** | Avoid module-level DB connections or cursors — not thread-safe |