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
        self.checkbox = None
        self.field_container1 = None
        self.field_container2 = None
        self.field_container3 = None
        self.field_container4 = None
        self.data = []
        self.pack(fill=BOTH, expand=YES)
        self.name = ttk.StringVar(value="")
        self.health = ttk.StringVar(value="")
        self.selection_var = ttk.StringVar(value="")
        self.initiative = ttk.DoubleVar(value=0)
        self.dex = ttk.DoubleVar(value=0)
        self.number_of_monsters = ttk.DoubleVar(value=0)
        self.checkbox_var = ttk.BooleanVar()
        self.colors = master_window.style.colors
        self.created_data = False
        self.created_data_monster = False
        self.created_data_player = False
        self.hp_tracker = False

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
        # Define Container
        selection_container = ttk.Frame(self)
        selection_container.pack(expand=YES, padx=(0, 100), pady=5, )

        # Create Label
        selection_label = ttk.Label(selection_container, text="Select type: ", width=15)
        selection_label.pack(side=LEFT, padx=5)

        # Add selection menu
        options = ["", "Monster", "Player"]  # List of options for the selection menu
        selection_menu = ttk.Combobox(selection_container, textvariable=self.selection_var, values=options)
        selection_menu.pack(side=LEFT, padx=2)

        selection_menu.bind("<<ComboboxSelected>>", self.on_select)  # Bind a function to selection event

    def create_buttonbox(self):
        # Define Container
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

    def create_form_entry(self, label, variable, is_monster=False, checkbox_callback=None):
        # Define container
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        # Create a Label
        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=12)

        # Create a checkbox if needed
        checkbox = None
        if is_monster:
            checkbox = ttk.Checkbutton(
                master=form_field_container,
                text="Group of Monsters",
                variable=self.checkbox_var,
                command=lambda: checkbox_callback(self.checkbox_var.get()) if checkbox_callback else None
            )
            checkbox.pack(side=BOTTOM, padx=(0, 155), pady=7)
            form_field_label.pack(side=LEFT, padx=12, pady=(3, 25))

        form_input = ttk.Entry(master=form_field_container, textvariable=variable, font=("Arial", 10))
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        return form_field_container, checkbox

    def create_table(self):
        # Define colum data
        colum_data = [
            {"text": "Name"},
            {"text": "Initiative roll", "stretch": False},
        ]

        # Extracting only Name and Initiative for display in the table
        display_data = [(entry[0], entry[1]) for entry in self.data]

        # Define/create Table
        table = Tableview(
            master=self,
            coldata=colum_data,
            rowdata=display_data,
            paginated=False,
            searchable=False,
            bootstyle="danger",
            stripecolor=(self.colors.dark, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=2, pady=10)

        return table

    def on_add(self):
        # Get values from input containers
        name = str(self.name.get())
        initiative = self.initiative.get()
        dex = self.dex.get()
        health_roll = str(self.health.get())
        selected_value = self.selection_var.get()

        # Check if it is a monster
        if selected_value == "Monster":
            # Check if it is a group of monsters
            checkbox_value = self.checkbox_var.get()
            if not checkbox_value:
                # Generate Monster values
                health, initiative = tray.roll_monster_data(health_roll, dex)
                print("Name: ", name)  # test print
                print("Health roll: ", health)  # test print
                print("Initiative roll: ", initiative)  # test print

                # Refresh table
                # noinspection PyTypeChecker
                self.table.insert_row("end", [name, initiative])
                self.table.load_table_data()
                self.data.append((name, initiative, dex, health))

            if checkbox_value:
                # Set group number to 1 if input container was left empty
                if self.number_of_monsters.get() == 0:
                    y = 1
                else:
                    y = int(self.number_of_monsters.get())

                # Generate Monster values for every monster in the group
                for x in range(y):
                    name = str(self.name.get()) + " " + str(x + 1)
                    health, initiative = tray.roll_monster_data(health_roll, dex)
                    print("Name: ", name)  # test print
                    print("Health roll: ", health)  # test print
                    print("Initiative roll: ", initiative)  # test print

                    # Refresh table
                    # noinspection PyTypeChecker
                    self.table.insert_row("end", [name, initiative])
                    self.table.load_table_data()
                    self.data.append((name, initiative, dex, health))

        # Add player data
        if selected_value == "Player":
            # Resolve a tie in initiative
            initiative = initiative + ((float(dex) + 10) / 100)

            print("Name: ", name)  # test print
            print("Initiative roll: ", initiative)  # test print

            # Refresh table
            # noinspection PyTypeChecker
            self.table.insert_row("end", [name, initiative])
            self.table.load_table_data()
            self.data.append((name, initiative, dex))

    def on_clear(self):

        # Destroy all Field containers
        if self.created_data:
            self.field_container1.destroy()
            self.field_container2.destroy()
            self.field_container3.destroy()
            if self.field_container4:
                self.field_container4.destroy()
            self.created_data = False
            self.created_data_player = False
            self.created_data_monster = False

        # Clear and recreate Table
        self.data = []
        self.table.destroy()
        self.table = self.create_table()

    def on_select(self, event):
        selected_value = self.selection_var.get()
        print("Selected:", selected_value)

        # Check if the "name" container is created
        if not self.created_data:
            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            # Create new containers
            self.field_container1, _ = self.create_form_entry("Name: ", self.name)
            self.created_data = True

            # Recreate table
            self.table = self.create_table()

        # Reset visuals when selecting nothing
        if selected_value == "":
            self.field_container1.destroy()
            self.field_container2.destroy()
            self.field_container3.destroy()
            if self.field_container4:
                self.field_container4.destroy()
            self.created_data = False
            self.created_data_monster = False
            self.created_data_player = False

        # Actions when "Player" is selected
        if selected_value == "Player":

            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            if self.created_data_monster:

                # Destroy Monster data
                self.field_container2.destroy()
                self.field_container3.destroy()
                if self.field_container4:
                    self.field_container4.destroy()
                self.created_data_monster = False

            if not self.created_data_player:
                # Create player data
                self.field_container2, _ = self.create_form_entry("DEX modifier: ", self.dex)
                self.field_container3, _ = self.create_form_entry("Initiative roll: ", self.initiative)
                self.created_data_player = True

            # Recreate the table
            self.table = self.create_table()

        # Actions when "Monster" is selected
        elif selected_value == "Monster":

            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            if self.created_data_player:
                # Destroy player data
                self.field_container2.destroy()
                self.field_container3.destroy()
                self.created_data_player = False

            if not self.created_data_monster:
                # Create Monster data
                self.field_container2, _ = self.create_form_entry("DEX modifier: ", self.dex)
                self.field_container3, self.checkbox = self.create_form_entry(
                    "Health: ",
                    self.health,
                    is_monster=True,
                    checkbox_callback=self.on_checkbox_checked
                )
                self.created_data_monster = True

            # Show checkbox
            self.checkbox.pack()

            # Recreate table
            self.table = self.create_table()

        elif hasattr(self, 'checkbox'):
            # Hide checkbox if it exists
            self.checkbox.pack_forget()

    def on_checkbox_checked(self, checkbox_value):
        if checkbox_value:
            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            # Create a new field container for group of monsters
            self.field_container4, _ = self.create_form_entry("#Monsters: ", self.number_of_monsters)
            self.field_container4.pack(fill=X, expand=YES, pady=5)

            # Recreate table
            self.table = self.create_table()

        else:
            # Destroy the field container if the checkbox is unchecked
            if hasattr(self, 'field_container4'):
                self.field_container4.destroy()


if __name__ == "__main__":
    app = ttk.Window("Initiative Tracker", "cyborg", resizable=(True, True))
    Tracker(app)  # Call the tracker function with the app argument
    app.mainloop()
