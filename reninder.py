"""Start a business logic."""
import tkinter as tk

# Create the root window
root = tk.Tk()

root.title("Reminder Application")

# Set fixed window size and make it non-resizable
root.geometry("450x400")
root.resizable(False, False)

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window on the screen
x_coordinate = int((screen_width / 2) - (450 / 2))
y_coordinate = int((screen_height / 2) - (400 / 2))

# Set the position of the window
root.geometry("+{}+{}".format(x_coordinate, y_coordinate))


# Create widgets
label1 = tk.Label(root, text="Label 1", height=2, width=10)
label2 = tk.Label(root, text="Label 2", height=2, width=10)
label3 = tk.Label(root, text="Label 3", height=2, width=10)
button1 = tk.Button(root, text="Button 1", height=2, width=10)
button2 = tk.Button(root, text="Button 2", height=2, width=10)
button3 = tk.Button(root, text="Button 3", height=2, width=10)
entry1 = tk.Entry(root, width=20)
entry2 = tk.Entry(root, width=20)
entry3 = tk.Entry(root, width=20)

# Add widgets to the grid
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)
label3.grid(row=0, column=2)
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)
button3.grid(row=1, column=2)
entry1.grid(row=2, column=0)
entry2.grid(row=2, column=1)
entry3.grid(row=2, column=2)

# Start the main loop
root.mainloop()
