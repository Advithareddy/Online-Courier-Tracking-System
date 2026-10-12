import sqlite3
import os

# Use Render's persistent disk when configured.
# Otherwise, use the local project database.
DATABASE = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "courier.db")
)

# Ensure the database directory exists.
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create all required database tables."""

    # Make sure database folder exists
    os.makedirs("database", exist_ok=True)

    connection = get_connection()
    cursor = connection.cursor()

    # =========================
    # USERS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # =========================
    # DRIVERS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            vehicle_number TEXT NOT NULL
        )
    """)

    # =========================
    # COURIERS TABLE
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS couriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            sender_name TEXT NOT NULL,
            sender_phone TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_phone TEXT NOT NULL,
            pickup_address TEXT NOT NULL,
            delivery_address TEXT NOT NULL,
            package_type TEXT NOT NULL,
            weight REAL,
            status TEXT DEFAULT 'Booked',
            latitude REAL,
            longitude REAL,
            driver_id INTEGER,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES drivers(id)
        )
    """)

    # =========================
    # ADD GPS COLUMNS TO
    # EXISTING DATABASE
    # =========================

    try:
        cursor.execute("""
            ALTER TABLE couriers
            ADD COLUMN latitude REAL
        """)
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("""
            ALTER TABLE couriers
            ADD COLUMN longitude REAL
        """)
    except sqlite3.OperationalError:
        pass

    # =========================
    # ADD DRIVER ID TO
    # EXISTING DATABASE
    # =========================

    try:
        cursor.execute("""
            ALTER TABLE couriers
            ADD COLUMN driver_id INTEGER
        """)
    except sqlite3.OperationalError:
        pass

    # =========================
    # SAVE CHANGES
    # =========================

    connection.commit()
    connection.close()

    print("Database tables created successfully!")


# =========================
# RUN DATABASE SETUP
# =========================

if __name__ == "__main__":
    create_tables()