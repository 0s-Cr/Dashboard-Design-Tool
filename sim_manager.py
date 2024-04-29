import can
from tkinter import *
from tkinter import ttk


class SimManager:
    def __init__(self, canvas):
        self.icon_list = []
        self.id_counter = 0
        self.canvas = canvas
        self.show_labels = False
        # Create variables for fault selections
        self.param_fault = None
        self.output_fault = None
        self.safety_fault = None
        self.bus_fault = None
        self.feedback_fault = None
        self.power_fault = None
        self.mtemp_fault = None
        self.dtemp_fault = None
        self.voltage_fault = None
        self.current_fault = None
        self.raceaway_fault = None
        self.user_fault = None
        self.cpu_fault = None
        self.ballast_fault = None
        self.power_warning = None
        self.mtemp_warning = None
        self.dtemp_warning = None
        self.voltage_warning = None
        self.current_warning = None
        self.overload_warning = None

    def __str__(self):
        return f"{self.icon_list}"

    def add_icon(self, icon):
        self.icon_list.append(icon)
        print(self.icon_list)

    def on_exit(self):
        for i in range(0, len(self.icon_list)):
            self.icon_list[i].kill_all()

    def toggle_true_false(self, value):
        if value == "On":
            return True
        else:
            return False

    def create_selections(self, frame):
        # Create the selection fields for faults to be transmitted over CAN (from the Bamocar Motor Controller)
        Label(frame, text="Fault Toggles:", bg="yellow").grid(row=0, column=0)
        Label(frame, text="Parameter Error").grid(row=1, column=0)
        self.param_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.param_fault.set("Off")
        self.param_fault.grid(row=1, column=1)

        Label(frame, text="Output Error").grid(row=2, column=0)
        self.output_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.output_fault.set("Off")
        self.output_fault.grid(row=2, column=1)

        Label(frame, text="Safety Circuit Error").grid(row=3, column=0)
        self.safety_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.safety_fault.set("Off")
        self.safety_fault.grid(row=3, column=1)

        Label(frame, text="Bus Transfer Error").grid(row=4, column=0)
        self.bus_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.bus_fault.set("Off")
        self.bus_fault.grid(row=4, column=1)

        Label(frame, text="Faulty Encoder Signal").grid(row=5, column=0)
        self.feedback_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.feedback_fault.set("Off")
        self.feedback_fault.grid(row=5, column=1)

        Label(frame, text="No Power Supply Voltage").grid(row=6, column=0)
        self.power_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.power_fault.set("Off")
        self.power_fault.grid(row=6, column=1)

        Label(frame, text="Motor Temperature Too High").grid(row=7, column=0)
        self.mtemp_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.mtemp_fault.set("Off")
        self.mtemp_fault.grid(row=7, column=1)

        Label(frame, text="Device Temperature Too High").grid(row=8, column=0)
        self.dtemp_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.dtemp_fault.set("Off")
        self.dtemp_fault.grid(row=8, column=1)

        Label(frame, text="Over Voltage").grid(row=9, column=0)
        self.voltage_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.voltage_fault.set("Off")
        self.voltage_fault.grid(row=9, column=1)

        Label(frame, text="Over Current").grid(row=10, column=0)
        self.current_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.current_fault.set("Off")
        self.current_fault.grid(row=10, column=1)

        Label(frame, text="Racing Error").grid(row=11, column=0)
        self.raceaway_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.raceaway_fault.set("Off")
        self.raceaway_fault.grid(row=11, column=1)

        Label(frame, text="User Defined Error").grid(row=12, column=0)
        self.user_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.user_fault.set("Off")
        self.user_fault.grid(row=12, column=1)

        Label(frame, text="Software Error").grid(row=13, column=0)
        self.cpu_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.cpu_fault.set("Off")
        self.cpu_fault.grid(row=13, column=1)

        Label(frame, text="Ballast Circuitry Overload").grid(row=14, column=0)
        self.current_fault = ttk.Combobox(frame, values=["On", "Off"])
        self.current_fault.set("Off")
        self.current_fault.grid(row=14, column=1)

        # Create a gap between faults and warnings
        Label(frame, text="").grid(row=15, column=0)
        Label(frame, text="Warning Toggles:", bg="red").grid(row=16, column=0)
        Label(frame, text="Voltage Warning").grid(row=17, column=0)
        self.power_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.power_warning.set("Off")
        self.power_warning.grid(row=17, column=1)

        Label(frame, text="Motor Temperature Critical").grid(row=18, column=0)
        self.mtemp_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.mtemp_warning.set("Off")
        self.mtemp_warning.grid(row=18, column=1)

        Label(frame, text="Device Temperature Critical").grid(row=19, column=0)
        self.dtemp_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.dtemp_warning.set("Off")
        self.dtemp_warning.grid(row=19, column=1)

        Label(frame, text="Critical Over Voltage").grid(row=20, column=0)
        self.voltage_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.voltage_warning.set("Off")
        self.voltage_warning.grid(row=20, column=1)

        Label(frame, text="Critical Over Current").grid(row=21, column=0)
        self.current_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.current_warning.set("Off")
        self.current_warning.grid(row=21, column=1)

        Label(frame, text="Over Load > 87%").grid(row=22, column=0)
        self.overload_warning = ttk.Combobox(frame, values=["On", "Off"])
        self.overload_warning.set("Off")
        self.overload_warning.grid(row=22, column=1)
