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



have to default allow :00 second and convert any second in to :00 in a Daily reminder update
and add a 0 before a hour if user not add like 02 hour in update
Handle SQLite Operation Error to table does not exist while Get data to display
when upload a CSV file before exist a table so getting error(no such table: daily_reminders)fix: create a connection to generate a .db file
Repeat same Db code again and again
------------------------------------
conn = sqlite3.connect("reminders.db")
c = conn.cursor()

Import many time from tkinter import ttk , fix it

on Server:
when we schedule a task for continue 3 minute so 2 popup will alert
