#access token
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

Daily task

id: an auto-incrementing primary key.
task: the text of the reminder.
reminder_datetime: the date and time the reminder should occur.


weekly task

id: an auto-incrementing primary key.
task: the text of the reminder.
day_of_week: the day of the week the reminder should occur, with 0 representing Monday.
reminder_datetime: the date and time the reminder should occur.

Monthly task

id: an auto-incrementing primary key.
task: the text of the reminder.
start_date: the date of the month when the reminder period starts, in the format "YYYY-MM-DD".
end_date: the date of the month when the reminder period ends, in the format "YYYY-MM-DD".
reminder_datetime: the date and time the reminder should occur.

Yearly task

id: an auto-incrementing primary key.
task: the text of the reminder.
month: the month of the year when the reminder should occur (1-12).
day_of_month: the day of the month when the reminder should occur (1-31).
reminder_datetime: the date and time the reminder should occur.



Important
----------
# create connection to database
        self.conn = sqlite3.connect("reminders.db")

        # create weekly_reminders table if it doesn't exist
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS weekly_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            day_of_week INTEGER NOT NULL,
            reminder_datetime DATETIME NOT NULL
            );
            """)
