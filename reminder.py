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
        # self.conn = conn
        # self.master.title("Time Selector")

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

        # self.daily_entry = tk.Entry(master)
        # self.daily_entry.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        # self.entry = tk.Entry(master)
        # self.entry.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

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
            if self.ampm_var.get() == "PM":
                hour += 12
            if hour == 24:
                hour = 0
            selected_time = time(hour=hour, minute=minute)
            # task = self.daily_entry.get()

            task = self.entry.get()
            print("Daily task #######", task)
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
        # except sqlite3.Error as e:
        #     messagebox.showerror("Database Error", f"An error occurred: {e}")

        except ValueError:
            print("Invalid time selected")

        # finally:
        #     self.conn.close()
        #     self.master.destroy()

    def daily_close_connection(self):
        """Close the DB connection."""
        conn.close()


class WeekdaySelector:
    """Weekly selector task class."""

    def __init__(self, master):
        """Start initialization for a weekly task."""
        self.master = master
        # self.master.title("Weekday Selector")
        # self.conn = conn
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
            if self.ampm_var.get() == "PM":
                hour += 12
            if hour == 24:
                hour = 0
            selected_time = time(hour=hour, minute=minute)

            # Get current date and time
            now = datetime.datetime.now()
            # Get the day of the week as an integer (Monday is 0 and Sunday is 6)
            day_of_week = now.weekday()
            print("Day of week in number", day_of_week)
            # Print the day of the week
            day = datetime.datetime.now().strftime("%A")
            print("Current name of Day in string", day)

            task = self.entry.get()
            print("Task to add DB", task)
            print("Day of number to add DB", selected_weekday)
            print("Day of week name to add DB", selected_day)
            print("Selected time to add DB", selected_time)
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
        # except sqlite3.Error as e:
        #     messagebox.showerror("Database Error", f"An error occurred: {e}")

        except ValueError:
            print("Invalid time selected")
        # selected_datetime += datetime.timedelta(days=(selected_weekday - selected_datetime.weekday() + 7) % 7)

        # finally:
        #     self.conn.close()
        #     self.master.destroy()

    def weekly_close_connection(self):
        """Close the DB connection."""
        conn.close()


class MonthSelector:
    """Monthly task selector class."""

    def __init__(self, master):
        """Start initialization for the monthly task."""
        print(master)
        self.master = master
        print("Dipesh parmar", self.master)

        # Create option menus for selecting day and month
        self.day_var = tk.StringVar(value="1")
        self.day_dropdown = tk.OptionMenu(
            master, self.day_var, *[str(i) for i in range(1, 32)]
        )

        self.month_var = tk.StringVar(value="January")
        self.month_dropdown = tk.OptionMenu(
            master,
            self.month_var,
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

        # Create submit button to get selected date
        self.submit_button = tk.Button(
            master, text="Submit", command=self.get_selected_date
        )

        # Grid the widgets
        self.day_dropdown.grid(row=0, column=0, padx=(10, 5))
        self.month_dropdown.grid(row=0, column=1, padx=(5, 10))
        self.submit_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

    def get_selected_date(
        self,
    ):
        """Convert selected date to python format."""
        try:
            # Convert selected day and month to Python date format
            day = int(self.day_var.get())
            month = datetime.strptime(self.month_var.get(), "%B").month
            year = datetime.now().year
            selected_date = datetime(year=year, month=month, day=day)

            # Do something with the selected date
            print(f"Selected date: {selected_date}")

        except ValueError:
            # if master.winfo_exists():
            # Handle invalid date input
            messagebox.showerror(
                "Invalid Date",
                f"\nPlease enter a valid date in the format 'Month Day' (e.g. January 1).\n You entered '{self.month_var.get()} {self.day_var.get()}'.",
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
        MonthSelector(root)

    # elif class_name == "Yearly":
    #     root = tk.Toplevel()
    #     app = Yearly(root)
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
# daily_selector = TimeSelector(root)
# week_selector = WeekdaySelector(root)
# daily_selector.daily_close_connection()
# week_selector.weekly_close_connection()
