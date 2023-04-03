"""Create a table for syatem."""
import sqlite3

# Connect to the database
with sqlite3.connect("reminders.db") as conn:

    # Create the daily reminders table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        reminder_datetime DATETIME NOT NULL
        );
        """
    )

    # Create the weekly reminders table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weekly_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        day_of_week INTEGER NOT NULL,
        day TEXT NULL,
        reminder_datetime DATETIME NOT NULL
        );
        """
    )

    # Create the monthly reminders table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS monthly_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NULL,
        reminder_datetime DATETIME NOT NULL
        );
        """
    )

    # Create the yearly reminders table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS yearly_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        month INTEGER NOT NULL,
        day_of_month INTEGER NOT NULL,
        reminder_datetime DATETIME NOT NULL
        );
        """
    )

    # Commit the changes
    conn.commit()

# Close the connection
conn.close()
