import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def sizegrip(self):
    # Create a size grip
    sizegrip_element = ttk.Sizegrip(self.master, style="light")
    sizegrip_element.pack(side="bottom", padx=5, pady=5, anchor="se")


def selection_menu(self, title, options=None):
    # Define Container
    selection_container = ttk.Frame(self)
    selection_container.pack(expand=NO, padx=(0, 100), pady=5, )

    # Create Label
    selection_label = ttk.Label(selection_container, text=title, width=15)
    selection_label.pack(side=LEFT, padx=5)

    # Add selection menu
    selection_menu_element = ttk.Combobox(selection_container, textvariable=self.selection_var, values=options)
    selection_menu_element.pack(side=LEFT, padx=2)

    selection_menu_element.bind("<<ComboboxSelected>>", self.on_select)  # Bind a function to selection event


def buttonbox(self, amount, names=None, command=None, style=None):
    # Define Container
    button_container = ttk.Frame(self)
    button_container.pack(fill=X, expand=NO, pady=(15, 10))

    for x in range(int(amount)):
        # Create button
        add_btn = ttk.Button(
            master=button_container,
            text=names[x - 1],
            command=command[x - 1],
            style=style[x - 1],
            width=1 + len(names[x - 1]),
        )
        add_btn.pack(side=RIGHT, padx=5)


def entry_field(self, title, variable, add_checkbox=False, checkbox1_callback=None, checkbox2_callback=None):
    # Define container
    form_field_container = ttk.Frame(self)
    form_field_container.pack(fill=X, expand=NO, pady=5)

    # Create a Label
    form_field_label = ttk.Label(master=form_field_container, text=title, width=15)
    form_field_label.pack(side=LEFT, padx=12)

    # Create a checkbox if needed
    checkbox_element1 = None
    checkbox_element2 = None
    if add_checkbox:
        checkbox_container = ttk.Frame(form_field_container)
        checkbox_element1 = checkbox(checkbox_container,
                                     "Group of Monsters",
                                     self.checkbox1_var,
                                     lambda: checkbox1_callback(
                                         self.checkbox1_var.get()) if checkbox1_callback else None)
        checkbox_element2 = checkbox(checkbox_container,
                                     "Group Initiative",
                                     self.checkbox2_var,
                                     None)
        # lambda: checkbox2_callback(self.checkbox2_var.get()) if checkbox2_callback else None)
        form_field_label.pack(side=LEFT, padx=12, pady=(0, 30))
        checkbox_container.pack(side=BOTTOM)

    # Create input field
    form_input = ttk.Entry(master=form_field_container, textvariable=variable, font=("Arial", 10))
    form_input.pack(side=LEFT, padx=5, fill=X, expand=NO)

    return form_field_container, checkbox_element1, checkbox_element2


def checkbox(master, title, variable, command):
    checkbox_element = ttk.Checkbutton(master=master, text=title, variable=variable, command=command)
    checkbox_element.pack(side=LEFT, padx=(0, 30), pady=7)

    return checkbox_element


def progressbar(self, container, title, health_roll):
    # Define container
    form_field_container = ttk.Frame(container)
    form_field_container.pack(fill=tk.X, expand=tk.YES, pady=5)

    # Create a Label
    form_field_label = ttk.Label(master=form_field_container, text=title, width=15)
    form_field_label.pack(side=tk.LEFT, padx=6)

    # Create progressbar
    form_field_bar = ttk.Progressbar(
        master=form_field_container,
        style="danger striped",
        mode="determinate",
        maximum=health_roll,
        length=200,
        value=health_roll,
    )
    form_field_bar.pack(side=tk.LEFT, padx=5)

    # Create input field
    form_input = ttk.Entry(master=form_field_container, textvariable=ttk.DoubleVar(value=0), font=("Arial", 10))
    form_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=tk.NO)

    # Create + button
    add_btn = ttk.Button(
        master=form_field_container,
        text="+",
        command=lambda: self.on_plus(form_input, form_field_bar),
        style="success",
        width=2,
    )
    add_btn.pack(side=LEFT, padx=5)

    # Create - button
    add_btn = ttk.Button(
        master=form_field_container,
        text="-",
        command=lambda: self.on_minus(form_input, form_field_bar),
        style="danger",
        width=2,
    )
    add_btn.pack(side=LEFT, padx=5)
