import json

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import create_elements as create


class HpWindow(ttk.Frame):

    # initiating all data
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.colors = master_window.style.colors
        self.pack(fill=BOTH, expand=YES)

        # Create a canvas to contain the progress bars
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Add a scrollbar to the right of the canvas
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the progress bars
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # Read data from the JSON file
        with open('shared_data.json', 'r') as file:
            data = json.load(file)

        # Create a health bar for each monster in the initiative
        for entry in data:
            if entry["status"] == "Monster":
                create.progressbar(self, frame, entry["name"], entry["health"])

        frame.update_idletasks()  # Update the size of the canvas

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        create.sizegrip(self)

    @staticmethod
    def on_plus(form_input, form_field_bar):
        # Get the current value from the entry field
        try:
            increment = float(form_input.get())  # Read the value from the Entry field
        except ValueError:
            # Handle the case where the input is not a valid number
            increment = 0

        new_value = form_field_bar['value'] + increment
        # Ensure the new value doesn't exceed the maximum value  x
        new_value = min(new_value, form_field_bar['maximum'])

        # Update the progress bar with the new value
        form_field_bar['value'] = new_value

    @staticmethod
    def on_minus(form_input, form_field_bar):
        # Get the current value from the entry field
        try:
            decrement = float(form_input.get())  # Read the value from the Entry field
        except ValueError:
            # Handle the case where the input is not a valid number
            decrement = 0

        new_value = form_field_bar['value'] - decrement
        # Ensure the new value doesn't go below zero
        new_value = max(new_value, 0)

        # Update the progress bar with the new value
        form_field_bar['value'] = new_value


if __name__ == "__main__":
    app = ttk.Window("Health Tracker", "vapor", size=[640, 500])
    HpWindow(app)  # Call the HpWindow function with the app argument
    app.mainloop()
