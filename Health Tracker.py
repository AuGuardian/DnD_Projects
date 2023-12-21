import json

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import create_elements as create


class HpWindow(ttk.Frame):

    # initiating all data
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.colors = master_window.style.colors
        self.pack(fill=BOTH, expand=YES)

        # Read data from the JSON file
        with open('shared_data.json', 'r') as file:
            data = json.load(file)

        # Create a health bar for each monster in the initiative
        for entry in data:
            if entry["status"] == "Monster":
                self.progressbar(entry["name"], entry["health"])

        create.sizegrip(self)

    def progressbar(self, title, health_roll):
        # Define container
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        # Create a Label
        form_field_label = ttk.Label(master=form_field_container, text=title, width=15)
        form_field_label.pack(side=LEFT, padx=6)

        # Create progressbar
        form_field_bar = ttk.Progressbar(master=form_field_container,
                                         style="danger striped",
                                         mode="determinate",
                                         maximum=health_roll,
                                         length=200,
                                         value=health_roll
                                         )
        form_field_bar.pack(side=LEFT, padx=5)

        # Create input field
        form_input = ttk.Entry(master=form_field_container, textvariable=ttk.DoubleVar(value=0), font=("Arial", 10))
        form_input.pack(side=LEFT, padx=5, fill=X, expand=NO)

        # Create buttons to change the HP-value
        create.buttonbox(self,
                         2,
                         ["+", "-"],
                         [lambda: self.on_plus(form_input, form_field_bar),
                          lambda: self.on_minus(form_input, form_field_bar)],
                         ["success", "danger"])

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
    app = ttk.Window("Health Tracker", "vapor",resizable=(True, True))
    HpWindow(app)  # Call the HpWindow function with the app argument
    app.mainloop()
