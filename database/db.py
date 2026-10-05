import sqlite3
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

DB_NAME = "spendly.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    """Open a connection to the SQLite database with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert sample data for development if not already present."""
    conn = get_db()
    try:
        # Check if users table already has data
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count > 0:
            return  # Already seeded

        # Hash the demo password
        password_hash = generate_password_hash("demo123")

        # Insert demo user
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash)
        )
        user_id = cursor.lastrowid

        # Current month start for spreading dates
        today = date.today()
        month_start = date(today.year, today.month, 1)

        # Sample expenses covering all categories, spread across the month
        sample_expenses = [
            (user_id, 25.50, "Food", month_start + timedelta(days=2), "Lunch with colleagues"),
            (user_id, 15.00, "Transport", month_start + timedelta(days=3), "Bus pass"),
            (user_id, 120.00, "Bills", month_start + timedelta(days=5), "Electricity bill"),
            (user_id, 45.00, "Health", month_start + timedelta(days=7), "Pharmacy"),
            (user_id, 30.00, "Entertainment", month_start + timedelta(days=10), "Movie tickets"),
            (user_id, 80.00, "Shopping", month_start + timedelta(days=12), "New shoes"),
            (user_id, 18.00, "Other", month_start + timedelta(days=15), "Gift"),
            (user_id, 22.00, "Food", month_start + timedelta(days=18), "Groceries"),
        ]

        for expense in sample_expenses:
            conn.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                (expense[0], expense[1], expense[2], expense[3].isoformat(), expense[4])
            )

        conn.commit()
    finally:
        conn.close()