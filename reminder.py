"""Start a business logic."""
import re
import os
import csv
import sqlite3
import threading
import tkinter as tk

from datetime import datetime, time
from tkinter import messagebox, filedialog


db_file = "reminders.db"

if not os.path.exists(db_file):
    # Create a new database file if it doesn't exist
    conn = sqlite3.connect(db_file)
    conn.close()


class TimeSelector:
    """Daily time selector."""

    def __init__(self, master):
        """Start initialization for a daily task."""
        self.master = master

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()

        self.lable = tk.Label(text="Daily Reminder")
        self.lable.grid(row=4, column=0)

        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")

        self.hour_options = [str(i).zfill(2) for i in range(1, 13)]
        self.minute_options = [str(i).zfill(2) for i in range(0, 60)]
        self.ampm_options = ["AM", "PM"]

        self.hour_dropdown = tk.OptionMenu(master, self.hour_var, *self.hour_options)
        self.minute_dropdown = tk.OptionMenu(
            master, self.minute_var, *self.minute_options
        )
        self.ampm_dropdown = tk.OptionMenu(master, self.ampm_var, *self.ampm_options)

        self.hour_dropdown.grid(row=0, column=1, padx=(10, 0))
        self.minute_dropdown.grid(row=0, column=2, padx=(5, 0))
        self.ampm_dropdown.grid(row=0, column=3, padx=(5, 10))

        # Create a label and input widget
        self.label = tk.Label(master, text="Enter your name:")
        self.label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        self.entry = tk.Entry(master)
        self.entry.grid()

        self.submit_button = tk.Button(
            master, text="Schedule", command=self.daily_submit
        )
        self.submit_button.grid(row=1, column=1, pady=(10, 0))

        self.submit_button = tk.Button(
            master, text="Import CSV", command=self.daily_csv
        )
        self.submit_button.grid(row=4, column=2, pady=(10, 0))

    def daily_csv(self):
        """Upload a csv file for a daily task."""
        # Open file dialog to select CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        # Read data from CSV file
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            rows = [row for row in reader]

        # Validate data
        errors = []
        for row in rows:
            if len(row) != 2:
                errors.append(f"Invalid row: {row}")
                continue

            task, reminder_datetime_str = row
            if not task:
                errors.append(f"Task missing: {row}")
                continue

            try:
                reminder_time = datetime.strptime(reminder_datetime_str, "%H:%M:%S")
                reminder_datetime = (
                    datetime.now()
                    .replace(
                        hour=reminder_time.hour,
                        minute=reminder_time.minute,
                        second=0,
                        microsecond=0,
                    )
                    .time()
                )
                reminder_datetime_str = reminder_datetime.strftime("%H:%M:%S")
            except ValueError:
                errors.append(f"Invalid datetime format: {row}")
                continue

            # Insert data into database
            with sqlite3.connect("reminders.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO daily_reminders (task, reminder_datetime)
                    VALUES (?, ?)
                    """,
                    (task, reminder_datetime_str),
                )

        if errors:
            messagebox.showerror("CSV Import Error", "\n".join(errors))
        else:
            messagebox.showinfo("CSV Import", "CSV import successful.")
        conn.commit()

    def daily_submit(self):
        """Create a submit btn."""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if self.ampm_var.get() == "PM" and hour != 12:
                hour += 12
            elif self.ampm_var.get() == "AM" and hour == 12:
                hour = 0
            selected_time = time(hour=hour, minute=minute)

            task = self.entry.get()
            # insert into daily_reminders table
            # conn = connect_to_db()
            # Use a context manager to handle the connection and cursor objects
            with sqlite3.connect("reminders.db") as conn:
                c = conn.cursor()

                # Create the daily reminders table
                c.execute(
                    """
                    CREATE TABLE IF NOT EXISTS daily_reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    reminder_datetime DATETIME NOT NULL
                    );
                    """
                )

                c.execute(
                    """
                    INSERT INTO daily_reminders (task, reminder_datetime)
                    VALUES (?, ?)
                """,
                    (task, selected_time.strftime("%H:%M:%S")),
                )

                # commit changes to the database
                conn.commit()

        except ValueError:
            print("Invalid time selected")

        except Exception as e:
            print("An error occurred:", str(e))


class WeekdaySelector:
    """Weekly selector task class."""

    def __init__(self, master):
        """Start initialization for a weekly task."""
        self.master = master

        # create weekday variable
        self.weekday_var = tk.StringVar()

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()

        self.lable = tk.Label(text="Daily Reminder")
        self.lable.grid(
            row=0,
            column=2,
        )

        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")

        self.hour_options = [str(i).zfill(2) for i in range(1, 13)]
        self.minute_options = [str(i).zfill(2) for i in range(0, 60, 5)]
        self.ampm_options = ["AM", "PM"]

        self.hour_dropdown = tk.OptionMenu(master, self.hour_var, *self.hour_options)
        self.minute_dropdown = tk.OptionMenu(
            master, self.minute_var, *self.minute_options
        )
        self.ampm_dropdown = tk.OptionMenu(master, self.ampm_var, *self.ampm_options)

        self.hour_dropdown.grid(row=2, column=1, padx=(10, 0))
        self.minute_dropdown.grid(row=2, column=2, padx=(5, 0))
        self.ampm_dropdown.grid(row=2, column=3, padx=(5, 10))

        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        # set default value for weekday
        self.weekday_var.set("Monday")

        # create weekday dropdown
        self.weekday_options = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        self.weekday_dropdown = tk.OptionMenu(
            master, self.weekday_var, *self.weekday_options
        )
        self.weekday_dropdown.grid(row=2, column=0, pady=10)

        self.entry = tk.Entry(master)
        self.entry.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))

        # create submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.convert)
        self.submit_button.grid(row=3, column=2, pady=10)

    def convert(self):
        """Convert selected day of week to Python format."""
        weekday_dict = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        selected_weekday = weekday_dict[self.weekday_var.get()]
        # iterate over the dictionary and check if the value matches the one we're looking for
        for key, value in weekday_dict.items():
            if value == selected_weekday:
                selected_day = key
                break
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if self.ampm_var.get() == "PM" and hour != 12:
                hour += 12
            elif self.ampm_var.get() == "AM" and hour == 12:
                hour = 0
            selected_time = time(hour=hour, minute=minute)

            task = self.entry.get()
            # conn = connect_to_db()
            with sqlite3.connect("reminders.db") as conn:
                c = conn.cursor()
                # Create the weekly reminders table
                c.execute(
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

                c.execute(
                    """
                    INSERT INTO weekly_reminders (task, day_of_week, day, reminder_datetime)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        task,
                        selected_weekday,
                        selected_day,
                        selected_time.strftime("%H:%M:%S"),
                    ),
                )

                # commit changes to the database
                conn.commit()

        except ValueError:
            print("Invalid time selected")

        except Exception as e:
            print("An error occurred:", str(e))


class MonthSelector:
    """Monthly task selector class."""

    def __init__(self, master):
        """Start initialization for the monthly task."""
        self.master = master
        master.title("Monthly Reminder")
        master.geometry("400x300")

        # Create label for displaying the result
        self.result_label = tk.Label(master, font=("Arial", 14))
        self.result_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()

        self.lable = tk.Label(text="Daily Reminder")
        self.lable.grid(row=4, column=0)

        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")

        self.hour_options = [str(i).zfill(2) for i in range(1, 13)]
        self.minute_options = [str(i).zfill(2) for i in range(0, 60, 5)]
        self.ampm_options = ["AM", "PM"]

        self.hour_dropdown = tk.OptionMenu(master, self.hour_var, *self.hour_options)
        self.minute_dropdown = tk.OptionMenu(
            master, self.minute_var, *self.minute_options
        )
        self.ampm_dropdown = tk.OptionMenu(master, self.ampm_var, *self.ampm_options)

        self.hour_dropdown.grid(row=0, column=1, padx=(10, 0))
        self.minute_dropdown.grid(row=0, column=2, padx=(5, 0))
        self.ampm_dropdown.grid(row=0, column=3, padx=(5, 10))

        # Create a label and input widget
        self.label = tk.Label(master, text="Enter your name:")
        self.label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        self.entry = tk.Entry(master)
        self.entry.grid()

        # Create label for start date selection
        self.select_start_label = tk.Label(
            master, text="Select a Start Date", font=("Arial", 14, "bold")
        )
        self.select_start_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

        # Create option menus for selecting start day and month
        self.start_day_var = tk.StringVar(value="1")
        self.start_day_dropdown = tk.OptionMenu(
            master, self.start_day_var, *[str(i) for i in range(1, 32)]
        )

        self.start_month_var = tk.StringVar(value="January")
        self.start_month_dropdown = tk.OptionMenu(
            master,
            self.start_month_var,
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

        # Create label for end date selection
        self.select_end_label = tk.Label(
            master, text="Select an End Date", font=("Arial", 14, "bold")
        )
        self.select_end_label.grid(row=2, column=0, padx=(10, 5), sticky="w")

        # Create option menus for selecting end day and month
        self.end_day_var = tk.StringVar(value="Select Day")
        self.end_day_dropdown = tk.OptionMenu(
            master, self.end_day_var, "Select Day", *[str(i) for i in range(1, 32)]
        )

        self.end_month_var = tk.StringVar(value="Select Month")

        self.end_month_dropdown = tk.OptionMenu(
            master,
            self.end_month_var,
            "Select Month",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

        # Create submit button to get selected dates
        self.submit_button = tk.Button(
            master, text="Submit", command=self.get_selected_date
        )

        # Grid the widgets
        self.start_day_dropdown.grid(row=1, column=0, padx=(10, 5), sticky="e")
        self.start_month_dropdown.grid(row=1, column=1, padx=(5, 10), sticky="w")
        self.end_day_dropdown.grid(row=3, column=0, padx=(10, 5), sticky="e")
        self.end_month_dropdown.grid(row=3, column=1, padx=(5, 10), sticky="w")
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def get_selected_date(self):
        """Get the selected start and end dates and display them."""
        end_day = self.end_day_var.get()
        end_month = self.end_month_var.get()
        if end_day != "Select Day" and end_month != "Select Month":
            try:
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                if self.ampm_var.get() == "PM" and hour != 12:
                    hour += 12
                elif self.ampm_var.get() == "AM" and hour == 12:
                    hour = 0
                reminder_datetime = time(hour=hour, minute=minute)

                x_day = int(self.start_day_var.get())
                x_month = datetime.strptime(self.start_month_var.get(), "%B").month
                x_year = datetime.now().year
                start_date = datetime(year=x_year, month=x_month, day=x_day).date()

                y_day = int(self.end_day_var.get())
                y_month = datetime.strptime(self.end_month_var.get(), "%B").month
                y_year = datetime.now().year
                end_date = datetime(year=y_year, month=y_month, day=y_day).date()

                if end_date < start_date:
                    messagebox.showerror(
                        "Invalid date range",
                        "End date cannot be earlier than start date.",
                    )
                else:
                    start_date_string = start_date.strftime("%B %d, %Y")
                    end_date_string = end_date.strftime("%B %d, %Y")

                    # need to save in db
                    start_date = datetime(year=x_year, month=x_month, day=x_day).date()

                    end_date = datetime(year=y_year, month=y_month, day=y_day).date()

                    task = self.entry.get()

                    self.result_label.config(
                        text=f"Selected start date: {start_date_string}\nSelected end date: {end_date_string}"
                    )

                    with sqlite3.connect("reminders.db") as conn:
                        c = conn.cursor()

                        # Create the monthly reminders table
                        c.execute(
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
                        c.execute(
                            """
                        INSERT INTO monthly_reminders (task, start_date, end_date, reminder_datetime)
                        VALUES (?, ?, ?, ?)""",
                            (
                                task,
                                start_date,
                                end_date,
                                reminder_datetime.strftime("%H:%M:%S"),
                            ),
                        )

                        conn.commit()

            except ValueError:
                # if master.winfo_exists():
                messagebox.showerror(
                    "Invalid date",
                    "Please select a valid date for start and end dates.",
                )

            except Exception as e:
                print("An error occurred:", str(e))
        else:
            try:
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                if self.ampm_var.get() == "PM" and hour != 12:
                    hour += 12
                elif self.ampm_var.get() == "AM" and hour == 12:
                    hour = 0
                reminder_datetime = time(hour=hour, minute=minute)

                x_day = int(self.start_day_var.get())
                x_month = datetime.strptime(self.start_month_var.get(), "%B").month
                x_year = datetime.now().year
                start_date = datetime(year=x_year, month=x_month, day=x_day).date()

                start_date_string = start_date.strftime("%B %d, %Y")

                # need to save in db
                start_date = datetime(year=x_year, month=x_month, day=x_day).date()

                task = self.entry.get()
                end_date = ""

                self.result_label.config(
                    text=f"Selected start date: {start_date_string}\n"
                )

                with sqlite3.connect("reminders.db") as conn:
                    c = conn.cursor()

                    # Create the monthly reminders table
                    c.execute(
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
                    c.execute(
                        """
                    INSERT INTO monthly_reminders (task, start_date, end_date, reminder_datetime)
                    VALUES (?, ?, ?, ?)""",
                        (
                            task,
                            start_date,
                            end_date,
                            reminder_datetime.strftime("%H:%M:%S"),
                        ),
                    )

                    conn.commit()

            except ValueError:
                # if master.winfo_exists():
                messagebox.showerror(
                    "Invalid date",
                    "Please select a valid date for start date only.",
                )

            except Exception as e:
                print("An error occurred:", str(e))

    def monthly_close_connection(self):
        """Close the DB connection."""
        conn.close()


class YearlySelector:
    """Create a yearly task scheduling."""

    def __init__(self, master):
        """Start initialization for a daily task."""
        self.master = master

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.ampm_var = tk.StringVar()

        self.lable = tk.Label(text="Daily Reminder")
        self.lable.grid(row=4, column=0)

        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")

        self.hour_options = [str(i).zfill(2) for i in range(1, 13)]
        self.minute_options = [str(i).zfill(2) for i in range(0, 60, 5)]
        self.ampm_options = ["AM", "PM"]

        self.hour_dropdown = tk.OptionMenu(master, self.hour_var, *self.hour_options)
        self.minute_dropdown = tk.OptionMenu(
            master, self.minute_var, *self.minute_options
        )
        self.ampm_dropdown = tk.OptionMenu(master, self.ampm_var, *self.ampm_options)

        self.hour_dropdown.grid(row=0, column=1, padx=(10, 0))
        self.minute_dropdown.grid(row=0, column=2, padx=(5, 0))
        self.ampm_dropdown.grid(row=0, column=3, padx=(5, 10))

        # Create a label and input widget
        self.label = tk.Label(master, text="Enter your name:")
        self.label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        self.entry = tk.Entry(master)
        self.entry.grid()

        # start the select a date for yearly and Create label for end date selection
        self.select_end_label = tk.Label(
            master, text="Select an End Date", font=("Arial", 14, "bold")
        )
        self.select_end_label.grid(row=3, column=0, padx=(10, 5), sticky="w")

        # Create option menus for selecting end day and month
        self.end_day_var = tk.StringVar(value="1")
        self.end_day_dropdown = tk.OptionMenu(
            master, self.end_day_var, *[str(i) for i in range(1, 32)]
        )

        self.end_month_var = tk.StringVar(value="January")
        self.end_month_dropdown = tk.OptionMenu(
            master,
            self.end_month_var,
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

        # Grid the widgets
        self.end_day_dropdown.grid(row=1, column=0, padx=(10, 5), sticky="e")
        self.end_month_dropdown.grid(row=1, column=1, padx=(5, 10), sticky="w")

        self.submit_button = tk.Button(
            master, text="Schedule", command=self.yearly_submit
        )
        self.submit_button.grid(row=1, column=2, pady=(10, 0))

    def yearly_submit(self):
        """Create a submit btn."""
        try:
            day = int(self.end_day_var.get())
            month = datetime.strptime(self.end_month_var.get(), "%B").month
            year = datetime.now().year
            datetime(year=year, month=month, day=day).date()

            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if self.ampm_var.get() == "PM" and hour != 12:
                hour += 12
            elif self.ampm_var.get() == "AM" and hour == 12:
                hour = 0
            selected_time = time(hour=hour, minute=minute)
            task = self.entry.get()

            with sqlite3.connect("reminders.db") as conn:
                c = conn.cursor()

                # Create the yearly reminders table
                c.execute(
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

                c.execute(
                    """
                    INSERT INTO yearly_reminders (task, month, day_of_month, reminder_datetime)
                    VALUES (?, ?, ?, ?)
                """,
                    (task, month, day, selected_time.strftime("%H:%M:%S")),
                )

                # commit changes to the database
                conn.commit()

        except ValueError:
            # if master.winfo_exists():
            messagebox.showerror(
                "Invalid date", "Please select a valid date for yearly reminder."
            )

        except Exception as e:
            print("An error occurred:", str(e))


def show_class_messagebox(class_name):
    """While clicking on option menu popup will appear."""
    # conn = sqlite3.connect("reminders.db")
    if class_name == "Daily":
        root = tk.Toplevel()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        popup_width = 400
        popup_height = 300
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        root.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        TimeSelector(root)

    elif class_name == "Weekly":
        root = tk.Toplevel()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        popup_width = 400
        popup_height = 300
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        root.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        WeekdaySelector(root)

    elif class_name == "Monthly":
        root = tk.Toplevel()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        popup_width = 400
        popup_height = 300
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        root.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        MonthSelector(root)

    elif class_name == "Yearly":
        root = tk.Toplevel()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        popup_width = 450
        popup_height = 300
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        root.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        YearlySelector(root)

    root.wait_window(root)


# interpreter_path = sys.executable

# # Run the reminders.py script to display reminders (in the background)
# subprocess.Popen([interpreter_path, "reminders.py"])


def check_daily_reminders():
    """Start the main logic, which will make us alert when the reminder will occur."""
    # Check for due reminders every minute
    while True:
        import time

        current_time = datetime.now().strftime("%H:%M") + ":00"
        try:
            conn = sqlite3.connect("reminders.db")
            # conn = connect_to_db()
            c = conn.cursor()
            c.execute(
                "SELECT * FROM daily_reminders WHERE reminder_datetime <= ?",
                (current_time,),
            )
            due_reminders = c.fetchall()
            for reminder in due_reminders:
                reminder_task = reminder[1]
                reminder_time = reminder[2]
                if reminder_time == current_time:
                    message = "Reminder: {}\n\nTime: {}".format(
                        reminder_task, reminder_time
                    )
                    root = tk.Tk()
                    root.withdraw()  # hide the main window
                    messagebox.showinfo("Reminder", message)
                    root.destroy()  # destroy the temporary window
            c.close()
            conn.close()
        except sqlite3.OperationalError as e:
            print("Table does not exist:", e)

        time.sleep(60)


def check_weekly_reminders():
    """Start the main logic, which will make us alert when the reminder will occur."""
    # Check for due reminders every minute
    while True:
        import time

        current_time = datetime.now().strftime("%H:%M") + ":00"
        try:
            conn = sqlite3.connect("reminders.db")
            # conn = connect_to_db()
            c = conn.cursor()

            # Execute a SELECT statement to retrieve specific columns from the table
            c.execute(
                "SELECT day_of_week, day, reminder_datetime FROM weekly_reminders"
            )
            data = c.fetchall()
            # Get current date and time
            now = datetime.now()

            # Get the day of the week as an integer (Monday is 0 and Sunday is 6)
            day_of_week = now.weekday()
            # Print the day of the week
            day = datetime.now().strftime("%A")

            # Check if there is a match in the retrieved data
            for reminder in data:
                if (
                    reminder[0] == day_of_week
                    and reminder[1] == day  # noqa: W503
                    and reminder[2] == current_time  # noqa: W503
                ):
                    # Display a pop-up message using tkinter
                    message = "Reminder: {}\n\nTime: {}".format(
                        reminder[1], reminder[2]
                    )
                    root = tk.Toplevel()
                    root.withdraw()  # hide the main window
                    messagebox.showinfo("Reminder", message)
                    root.destroy()  # destroy the temporary window

            c.close()
            conn.close()
        except sqlite3.OperationalError as e:
            print("Table does not exist:", e)

        time.sleep(60)


def check_monthly_reminders():
    """Start the main logic, which will make us alert when the reminder will occur."""
    # Check for due reminders every minute
    while True:
        import time

        current_time = datetime.now().strftime("%H:%M") + ":00"
        try:
            conn = sqlite3.connect("reminders.db")
            # conn = connect_to_db()
            c = conn.cursor()
            c.execute(
                "SELECT * FROM daily_reminders WHERE reminder_datetime <= ?",
                (current_time,),
            )
            due_reminders = c.fetchall()
            for reminder in due_reminders:
                reminder_task = reminder[1]
                reminder_time = reminder[2]
                if reminder_time == current_time:
                    message = "Reminder: {}\n\nTime: {}".format(
                        reminder_task, reminder_time
                    )
                    root = tk.Toplevel()
                    root.withdraw()  # hide the main window
                    messagebox.showinfo("Reminder", message)
                    root.destroy()  # destroy the temporary window
            c.close()
            conn.close()
        except sqlite3.OperationalError as e:
            print("Table does not exist:", e)

        time.sleep(60)


def check_yearly_reminder():
    """Start the yearly reminder for once in a year."""
    while True:
        import time

        current_time = datetime.now().strftime("%H:%M") + ":00"
        try:
            # create a connection to the database
            conn = sqlite3.connect("reminders.db")

            # get the current date
            now = datetime.now()

            # select all reminders from the yearly_reminders table
            c = conn.cursor()
            c.execute("SELECT * FROM yearly_reminders")
            reminders = c.fetchall()

            # loop through the reminders and compare with the current date
            for reminder in reminders:
                month = reminder[2]
                day = reminder[3]
                occur = reminder[4]

                # check if the month and day match the current date
                if month == now.month and day == now.day and current_time == occur:
                    # display a reminder message box
                    message = "Reminder: {}\n\nTime: {}".format(
                        reminder[1],
                        occur,
                    )

                    root = tk.Tk()
                    root.withdraw()  # hide the main window
                    messagebox.showinfo("Yearly Reminder", message)
                    root.destroy()  # destroy the temporary window

            c.close()
            conn.close()
        except sqlite3.OperationalError as e:
            print("Table does not exist:", e)

        time.sleep(60)


def set_popup_geometry(root):
    """Set tha common function for a popup."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    popup_width = 600
    popup_height = 400
    x_position = (screen_width - popup_width) // 2
    y_position = (screen_height - popup_height) // 2
    root.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")


def show_daily_window():
    """Display a daily data on a window."""
    daily_root = tk.Toplevel()
    daily_root.title("Daily Task Window")
    set_popup_geometry(daily_root)

    from tkinter import ttk

    # Create treeview
    tree = ttk.Treeview(
        daily_root, columns=("id", "task", "reminder_datetime"), show="headings"
    )
    tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Define column headings
    tree.heading("id", text="ID")
    tree.heading("task", text="Task")
    tree.heading("reminder_datetime", text="Reminder Date Time")

    # Fetch data from daily_reminders table
    conn = sqlite3.connect("reminders.db")
    c = conn.cursor()
    c.execute("SELECT id, task, reminder_datetime FROM daily_reminders")
    rows = c.fetchall()

    # Insert data into treeview
    for row in rows:
        tree.insert("", tk.END, values=row)
        tree.selection()

    # Define update function
    def update_selected():
        """Update a selected daily data."""
        try:
            selected_row_id = tree.selection()[0]
        except IndexError:
            messagebox.showwarning("Error", "Please select a row to update.")
            return

        selected_row = tree.item(selected_row_id)
        current_values = selected_row["values"]

        # Create popup window for updating task and time
        update_popup = tk.Toplevel()
        update_popup.title("Update Task")
        update_popup.geometry("300x200")

        # Task field
        tk.Label(update_popup, text="Task:").grid(row=0, column=0, padx=10, pady=10)
        task_entry = tk.Entry(update_popup)
        task_entry.insert(tk.END, current_values[1])
        task_entry.grid(row=0, column=1, padx=10, pady=10)

        # Time field
        tk.Label(update_popup, text="Time (HH:MM):").grid(
            row=1, column=0, padx=10, pady=10
        )
        time_entry = tk.Entry(update_popup)
        time_entry.insert(tk.END, current_values[2])
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # Save button
        def save_changes():
            """Save a updated daily data to db."""
            # Validate time format
            try:
                datetime.strptime(time_entry.get(), "%H:%M:%S")
            except ValueError:
                messagebox.showwarning("Error", "Please enter a valid time (HH:MM).")
                return

            # Update record in database
            new_values = (task_entry.get(), time_entry.get(), current_values[0])
            c.execute(
                "UPDATE daily_reminders SET task = ?, reminder_datetime = ? WHERE id = ?",
                new_values,
            )
            conn.commit()

            # Update treeview
            tree.item(
                selected_row_id,
                values=(current_values[0], task_entry.get(), time_entry.get()),
            )
            update_popup.destroy()

        tk.Button(update_popup, text="Save", command=save_changes).grid(
            row=2, column=0, columnspan=2, padx=10, pady=10
        )

    # Update button
    tk.Button(daily_root, text="Update", command=update_selected).grid(
        row=1, column=0, padx=10, pady=10
    )

    def delete_selected():
        """Delete a selected data in a db."""
        selected_row_id = tree.selection()
        if not selected_row_id:
            messagebox.showerror("Error", "No row selected")
            return

        # Confirm deletion
        confirmation = messagebox.askyesno(
            "Confirmation",
            "Are you sure you want to delete the selected row?",
            icon="question",
        )
        if not confirmation:
            return

        selected_row_id = selected_row_id[0]
        tree.delete(selected_row_id)

        # Extract integer id from selected row id
        id_match = re.search(r"\d+", selected_row_id)
        if not id_match:
            messagebox.showerror("Error", "Invalid row id")
            return
        row_id = id_match.group()

        # Delete the row from the database
        conn = sqlite3.connect("reminders.db")
        c = conn.cursor()
        c.execute("DELETE FROM daily_reminders WHERE id=?", (row_id,))
        conn.commit()
        conn.close()

    delete_button = ttk.Button(daily_root, text="Delete", command=delete_selected)
    delete_button.grid(row=3, column=0, pady=10)


def show_weekly_window():
    """Set weekly data to display on a window."""
    weekly_root = tk.Toplevel()
    weekly_root.title("Weekly Task Window")
    set_popup_geometry(weekly_root)


def show_monthly_window():
    """Show a monthly data."""
    monthly_root = tk.Toplevel()
    monthly_root.title("Monthly Task Window")
    set_popup_geometry(monthly_root)


def show_yearly_window():
    """Set yearly data to display on a window."""
    yearly_root = tk.Toplevel()
    yearly_root.title("Yearly Task Window")
    set_popup_geometry(yearly_root)


if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()

    # Set up option menu
    options = ["Daily", "Weekly", "Monthly", "Yearly"]
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])
    option_menu = tk.OptionMenu(root, selected_option, *options)
    option_menu.grid(row=10, column=0, padx=80, pady=(0, 20), sticky="ew")

    # Set up button
    button = tk.Button(
        root,
        text="Select",
        command=lambda: show_class_messagebox(selected_option.get()),
    )
    button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="e")

    # Create an option menu with task options
    task_options = ["Daily Task", "Weekly Task", "Monthly Task", "Yearly Task"]
    selected_task = tk.StringVar(value=task_options[0])
    option_menu = tk.OptionMenu(root, selected_task, *task_options)
    option_menu.grid()

    # Create a button to open the selected task window
    open_task_button = tk.Button(
        root,
        text="Open Task",
        command=lambda: {
            "Daily Task": show_daily_window,
            "Weekly Task": show_weekly_window,
            "Monthly Task": show_monthly_window,
            "Yearly Task": show_yearly_window,
        }[selected_task.get()](),
    )
    open_task_button.grid()

    # Set up window properties
    root.title("Reminder Application")
    root.geometry("450x400")
    root.resizable(False, False)

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (450 / 2))
    y_coordinate = int((screen_height / 2) - (400 / 2))
    root.geometry("+{}+{}".format(x_coordinate, y_coordinate))

    daily_thread = threading.Thread(target=check_daily_reminders)
    weekly_thread = threading.Thread(target=check_weekly_reminders)
    yearly_thread = threading.Thread(target=check_yearly_reminder)
    daily_thread.start()
    weekly_thread.start()
    yearly_thread.start()

    root.mainloop()
