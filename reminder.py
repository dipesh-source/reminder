"""Start a business logic."""
import tkinter as tk
import sqlite3

from datetime import datetime, time
from pydub import AudioSegment
from pydub.playback import play
from tkinter import messagebox


conn = sqlite3.connect("reminders.db")


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

        self.submit_button = tk.Button(
            master, text="Schedule", command=self.daily_submit
        )
        self.submit_button.grid(row=1, column=1, pady=(10, 0))

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
            print("testing the daily types", type(selected_time))

            task = self.entry.get()
            print(selected_time, "Daily task #######", task)
            # insert into daily_reminders table
            conn = sqlite3.connect("reminders.db")  # re-open the connection
            conn.execute(
                """
                INSERT INTO daily_reminders (task, reminder_datetime)
                VALUES (?, ?)
            """,
                (task, selected_time.strftime("%H:%M:%S")),
            )

            # commit changes to the database
            conn.commit()
            conn.close()
            # Load and play a sound file when the button is clicked
            sound = AudioSegment.from_file("play.wav", format="wav")
            play(sound)

        except ValueError:
            print("Invalid time selected")

    def daily_close_connection(self):
        """Close the DB connection."""
        conn.close()


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

            # Get current date and time
            now = datetime.now()
            # Get the day of the week as an integer (Monday is 0 and Sunday is 6)
            day_of_week = now.weekday()
            print("Day of week in number", day_of_week)
            # Print the day of the week
            day = datetime.now().strftime("%A")
            print("Current name of Day in string", day)

            task = self.entry.get()
            conn = sqlite3.connect("reminders.db")  # re-open the connection
            conn.execute(
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
            conn.close()

        except ValueError:
            print("Invalid time selected")

    def weekly_close_connection(self):
        """Close the DB connection."""
        conn.close()


class MonthSelector:
    """Monthly task selector class."""

    def __init__(self, master):
        """Start initialization for the monthly task."""
        print(master)
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
        start_day = self.start_day_var.get()
        start_month = self.start_month_var.get()

        end_day = self.end_day_var.get()
        end_month = self.end_month_var.get()

        try:

            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if self.ampm_var.get() == "PM" and hour != 12:
                hour += 12
            elif self.ampm_var.get() == "AM" and hour == 12:
                hour = 0
            reminder_datetime = time(hour=hour, minute=minute)
            print("Selected time from the monthly task", reminder_datetime)

            # x_day = int(self.start_day_var.get())
            # x_month = datetime.strptime(self.start_month_var.get(), "%B").month
            # x_year = datetime.now().year
            # x_selected_date = datetime(year=x_year, month=x_month, day=x_day).date()
            # print("selected_date **************", x_selected_date)

            # y_day = int(self.end_day_var.get())
            # y_month = datetime.strptime(self.end_month_var.get(), "%B").month
            # y_year = datetime.now().year
            # y_selected_date = datetime(year=y_year, month=y_month, day=y_day).date()
            # print("selected_date **************", y_selected_date)

            start_date = datetime.strptime(
                f"{start_month} {start_day} 2023", "%B %d %Y"
            ).date()
            end_date = datetime.strptime(
                f"{end_month} {end_day} 2023", "%B %d %Y"
            ).date()
            print("Chat GPT start_date ********", start_date)
            print("Chat GPT end_date ********", end_date)

            if end_date < start_date:
                messagebox.showerror(
                    "Invalid date range",
                    "End date cannot be earlier than start date.",
                )
            else:
                start_date_string = start_date.strftime("%B %d, %Y")
                end_date_string = end_date.strftime("%B %d, %Y")

                # need to save in db
                start_date = datetime.strptime(
                    f"{start_month} {start_day} 2023", "%B %d %Y"
                ).date()
                end_date = datetime.strptime(
                    f"{end_month} {end_day} 2023", "%B %d %Y"
                ).date()

                task = self.entry.get()

                self.result_label.config(
                    text=f"Selected start date: {start_date_string}\nSelected end date: {end_date_string}"
                )

                # re-open the connection
                conn = sqlite3.connect("reminders.db")
                conn.execute(
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
                conn.close()

        except ValueError:
            # if master.winfo_exists():
            messagebox.showerror(
                "Invalid date", "Please select a valid date for start and end dates."
            )

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

            conn = sqlite3.connect("reminders.db")  # re-open the connection
            conn.execute(
                """
                INSERT INTO yearly_reminders (task, month, day_of_month, reminder_datetime)
                VALUES (?, ?, ?, ?)
            """,
                (task, month, day, selected_time.strftime("%H:%M:%S")),
            )

            # commit changes to the database
            conn.commit()
            conn.close()

            # Load and play a sound file when the button is clicked
            sound = AudioSegment.from_file("play.wav", format="wav")
            play(sound)
        except ValueError:
            # if master.winfo_exists():
            messagebox.showerror(
                "Invalid date", "Please select a valid date for yearly reminder."
            )


def show_class_messagebox(class_name):
    """While clicking on option menu popup will appear."""
    # conn = sqlite3.connect("reminders.db")
    if class_name == "Daily":
        root = tk.Toplevel()
        daily_selector = TimeSelector(root)
        daily_selector.daily_close_connection()

        # screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()
        # root.geometry(f"300x200+{screen_width//2-150}+{screen_height//2-100}")
        # root.protocol("WM_DELETE_WINDOW", daily_selector.daily_close_connection) # close connection when window is closed

    elif class_name == "Weekly":
        root = tk.Toplevel()
        week_selector = WeekdaySelector(root)
        week_selector.weekly_close_connection()

    elif class_name == "Monthly":
        root = tk.Toplevel()
        monthly_selector = MonthSelector(root)
        monthly_selector.monthly_close_connection()

    elif class_name == "Yearly":
        root = tk.Toplevel()
        YearlySelector(root)
    root.wait_window(root)


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
    root, text="Select", command=lambda: show_class_messagebox(selected_option.get())
)
button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="e")

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

root.mainloop()
