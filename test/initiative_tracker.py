import json
import subprocess
import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

import create_elements as create
import conversion as convert
import dice_tray as tray


def on_health():
    # Create and start a thread for the second window
    hp_window_thread = threading.Thread(target=run_script)
    hp_window_thread.start()


def run_script():
    subprocess.run(["C:/Users/S.Baplu/PycharmProjects/Initiative Tracker app/Health Tracker.exe"])


class Tracker(ttk.Frame):

    # initiating all data
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.colors = master_window.style.colors

        self.field_container1 = None
        self.field_container2 = None
        self.field_container3 = None
        self.field_container4 = None
        self.checkbox1 = None
        self.checkbox2 = None
        self.checkbox1_var = ttk.BooleanVar()
        self.checkbox2_var = ttk.BooleanVar()

        self.data = []
        self.name = ttk.StringVar(value="")
        self.health = ttk.StringVar(value="")
        self.selection_var = ttk.StringVar(value="")
        self.initiative = ttk.DoubleVar(value=0)
        self.dex = ttk.DoubleVar(value=0)
        self.number_of_monsters = ttk.DoubleVar(value=0)

        self.created_data = False
        self.created_data_monster = False
        self.created_data_player = False
        self.hp_tracker = False

        # Add Title info
        instruction_text = "Enter the creature's info and click Add"
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=6)

        # Create objects
        create.selection_menu(self, "Select type: ", options=["", "Monster", "Player"])
        create.buttonbox(self, 3,
                         ["Add", "Clear", "HP-Tracker"],
                         [self.on_add, self.on_clear, on_health],
                         ["success", "danger", "primary"])
        self.table = self.create_table()
        create.sizegrip(self)

        # Reset json file
        formatted_data = convert.data_to_json(self.data)

        # Write the formatted data to a JSON file to empty it
        with open('shared_data.json', 'w') as file:
            json.dump(formatted_data, file, indent=4)

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
            # Check if it is a group of monsters and if they have a group initiative
            checkbox1_value = self.checkbox1_var.get()
            checkbox2_value = self.checkbox2_var.get()
            if not checkbox1_value:
                # Generate Monster values
                health, initiative = tray.roll_monster_data(health_roll, dex)

                # Refresh table
                # noinspection PyTypeChecker
                self.table.insert_row("end", [name, initiative])
                self.table.load_table_data()

                # Update data
                self.data.append((name, initiative, dex, health, selected_value))
                formatted_data = convert.data_to_json(self.data)

                # Write the formatted data to a JSON file
                with open('shared_data.json', 'w') as file:
                    json.dump(formatted_data, file, indent=4)

            if checkbox1_value:
                # Set group number to 1 if input container was left empty
                if self.number_of_monsters.get() == 0:
                    y = 1
                else:
                    y = int(self.number_of_monsters.get())

                # Roll group initiative if active
                if checkbox2_value:
                    initiative = tray.initiative_roll(dex)

                # Generate Monster values for every monster in the group
                for x in range(y):
                    name = str(self.name.get()) + " " + str(x + 1)
                    health = 0

                    # only roll health when group initiative is active
                    if not checkbox2_value:
                        health, initiative = tray.roll_monster_data(health_roll, dex)
                    elif checkbox2_value:
                        health, _ = tray.roll_monster_data(health_roll, dex)

                    # Refresh table
                    # noinspection PyTypeChecker
                    self.table.insert_row("end", [name, initiative])
                    self.table.load_table_data()

                    # Update data
                    self.data.append((name, initiative, dex, health, selected_value))
                    formatted_data = convert.data_to_json(self.data)

                    # Write the formatted data to a JSON file
                    with open('shared_data.json', 'w') as file:
                        json.dump(formatted_data, file, indent=4)

        # Add player data
        if selected_value == "Player":
            # Resolve a tie in initiative
            initiative = initiative + ((float(dex) + 10) / 100)

            # Refresh table
            # noinspection PyTypeChecker
            self.table.insert_row("end", [name, initiative])
            self.table.load_table_data()

            # Update data
            self.data.append((name, initiative, dex, 0, selected_value))
            formatted_data = convert.data_to_json(self.data)

            # Write the formatted data to a JSON file
            with open('shared_data.json', 'w') as file:
                json.dump(formatted_data, file, indent=4)

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
        self.data.clear()
        self.table.destroy()
        self.table = self.create_table()

        # Reset json file
        formatted_data = convert.data_to_json(self.data)

        # Write the formatted data to a JSON file to empty it
        with open('shared_data.json', 'w') as file:
            json.dump(formatted_data, file, indent=4)

    def on_select(self, event):
        selected_value = self.selection_var.get()

        # Check if the "name" container is created
        if not self.created_data:
            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            # Create new containers
            self.field_container1, _, _ = create.entry_field(self, "Name: ", self.name)
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
                self.field_container2, _, _ = create.entry_field(self, "DEX modifier: ", self.dex)
                self.field_container3, _, _ = create.entry_field(self, "Initiative roll: ", self.initiative)
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
                self.field_container2, _, _ = create.entry_field(self, "DEX modifier: ", self.dex)
                self.field_container3, self.checkbox1, self.checkbox2 = create.entry_field(
                                                                        self,
                                                                        "Health: ",
                                                                        self.health,
                                                                        add_checkbox=True,
                                                                        checkbox1_callback=self.on_checkbox1_checked
                                                                        )
                self.created_data_monster = True

            # Show checkbox
            self.checkbox1.pack()
            self.checkbox2.pack()

            # Recreate table
            self.table = self.create_table()

        elif hasattr(self, 'checkbox'):
            # Hide checkbox if it exists
            self.checkbox1.pack_forget()
            self.checkbox2.pack_forget()

    def on_checkbox1_checked(self, checkbox_value):
        if checkbox_value:
            # Destroy the table so the visual order doesn't change
            self.table.destroy()

            # Create a new field container for group of monsters
            self.field_container4, _, _ = create.entry_field(self, "#Monsters: ", self.number_of_monsters)
            self.field_container4.pack(fill=X, expand=NO, pady=5)

            # Recreate table
            self.table = self.create_table()

        else:
            # Destroy the field container if the checkbox is unchecked
            if hasattr(self, 'field_container4'):
                self.field_container4.destroy()


if __name__ == "__main__":
    app = ttk.Window("Initiative Tracker", "cyborg", resizable=(True, True))
    Tracker(app)  # Call the Tracker function with the app argument
    app.mainloop()
