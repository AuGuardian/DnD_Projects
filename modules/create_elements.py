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


def entry_field(self, title, variable, and_checkbox=False, checkbox_callback=None):
    # Define container
    form_field_container = ttk.Frame(self)
    form_field_container.pack(fill=X, expand=NO, pady=5)

    # Create a Label
    form_field_label = ttk.Label(master=form_field_container, text=title, width=15)
    form_field_label.pack(side=LEFT, padx=12)

    # Create a checkbox if needed
    checkbox_element = None
    if and_checkbox:
        checkbox_element = checkbox(form_field_container,
                                    "Group of Monsters",
                                    self.checkbox_var,
                                    lambda: checkbox_callback(self.checkbox_var.get()) if checkbox_callback else None)
        form_field_label.pack(side=LEFT, padx=12, pady=(3, 25))

    # Create input field
    form_input = ttk.Entry(master=form_field_container, textvariable=variable, font=("Arial", 10))
    form_input.pack(side=LEFT, padx=5, fill=X, expand=NO)

    return form_field_container, checkbox_element


def checkbox(master, title, variable, command):
    checkbox_element = ttk.Checkbutton(master=master, text=title, variable=variable, command=command)
    checkbox_element.pack(side=BOTTOM, padx=(0, 155), pady=7)

    return checkbox_element


def scrollbar(canvas, app):
    # Create a vertical scrollbar
    scrollbar_element = ttk.Scrollbar(app, orient=VERTICAL, command=canvas.yview)
    scrollbar_element.pack(side=RIGHT, fill=Y)

    # Configure the canvas to interact with the scrollbar
    canvas.config(yscrollcommand=scrollbar_element.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    return scrollbar_element
