import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import dice_tray as tray


class Tracker(ttk.Frame):

    def add_sizegrip(self):
        # Create a size grip
        sizegrip = ttk.Sizegrip(self.master, style="light")
        sizegrip.pack(side="bottom", padx=5, pady=5, anchor="se")

    # initiating all data
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.field_container1 = None
        self.field_container2 = None
        self.field_container3 = None
        self.pack(fill=BOTH, expand=YES)
        self.name = ttk.StringVar(value="")
        self.health = ttk.StringVar(value="")
        self.selection_var = ttk.StringVar(value="")
        self.initiative = ttk.DoubleVar(value=0)
        self.colors = master_window.style.colors
        self.created_data = False
        self.created_data_health = False

        # Add Title info
        instruction_text = "Enter the creature's info and click Add"
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=6)

        # Create objects
        self.create_selection_menu()
        self.create_buttonbox()
        self.table = self.create_table()
        self.add_sizegrip()

    def create_selection_menu(self):
        selection_container = ttk.Frame(self)
        selection_container.pack(expand=YES, padx=(0, 100), pady=5,)

        selection_label = ttk.Label(selection_container, text="Select Type: ", width=15)
        selection_label.pack(side=LEFT, padx=5)

        options = ["", "Monster", "Player"]  # List of options for the selection menu
        selection_menu = ttk.Combobox(selection_container, textvariable=self.selection_var, values=options)
        selection_menu.pack(side=LEFT, padx=2)

        selection_menu.bind("<<ComboboxSelected>>", self.on_select)  # Bind a function to selection event

    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        # Create "Add" button
        add_btn = ttk.Button(
            master=button_container,
            text="Add",
            command=self.on_add,
            style="success",
            width=6,
        )
        add_btn.pack(side=RIGHT, padx=5)

        # Create "Clear" button
        clear_btn = ttk.Button(
            master=button_container,
            text="Clear",
            command=self.on_clear,
            style="danger",
            width=6,
        )
        clear_btn.pack(side=RIGHT, padx=5)

    def create_form_entry(self, label, variable):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=12)

        form_input = ttk.Entry(master=form_field_container, textvariable=variable, font=("Arial", 10))
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        return form_field_container

    def create_table(self):
        colum_data = [
            {"text": "Name"},
            {"text": "Initiative roll", "stretch": False},
        ]

        table = Tableview(
            master=self,
            coldata=colum_data,
            paginated=False,
            searchable=False,
            bootstyle="danger",
            stripecolor=(self.colors.dark, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=2, pady=10)

        return table

    def on_add(self):
        name = str(self.name.get())
        initiative = self.initiative.get()
        health_roll = str(self.health.get())
        selected_value = self.selection_var.get()

        # test print
        print("Name:", name)
        print("Initiative roll: ", initiative)

        # roll the health of the monster
        if selected_value == "Monster":
            health = tray.dice_roll(health_roll)
            print("Health roll: ", health)  # test print

        # Refresh table
        self.table.insert_row("end", [name, initiative])
        self.table.load_table_data()

    def on_clear(self):

        # Destroy all Field containers
        if self.created_data:
            self.field_container1.destroy()
            self.field_container2.destroy()
            self.created_data = False
            if self.created_data_health:
                self.field_container3.destroy()
                self.created_data_health = False

        # Clear and recreate Table
        self.table.destroy()
        self.table = self.create_table()

    def on_select(self, event):
        selected_value = self.selection_var.get()
        print("Selected:", selected_value)

        if not self.created_data:
            # Destroy Table so visual order doesn't change
            self.table.destroy()

            # Create new containers
            self.field_container1 = self.create_form_entry("Name: ", self.name)
            self.field_container2 = self.create_form_entry("Initiative roll: ", self.initiative)
            self.created_data = True

            # Recreate table
            self.table = self.create_table()

        if selected_value == "Player":

            # Destroy Health container
            if self.created_data_health:
                self.field_container3.destroy()
                self.created_data_health = False



        elif selected_value == "Monster":
            # Destroy Table so visual order doesn't change
            self.table.destroy()

            # Create Health container
            self.field_container3 = self.create_form_entry("Health: ", self.health)
            self.created_data_health = True

            # Recreate table
            self.table = self.create_table()


if __name__ == "__main__":
    app = ttk.Window("Initiative Tracker", "cyborg", resizable=(True, True))
    Tracker(app)  # Call the tracker function with the app argument
    app.mainloop()
