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
        # TODO find a more efficient way to do this
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
        # Bind event to comboboxes
        self.all_comboboxes = []
        self.can_message_data = []

    def __str__(self):
        return f"{self.icon_list}"

    def add_icon(self, icon):
        self.icon_list.append(icon)

    def on_exit(self):
        for i in range(0, len(self.icon_list)):
            self.icon_list[i].kill_all()

    def update_dials(self, channel, percentage):
        for i in self.icon_list:
            if hasattr(i.shape, "channel") and i.shape.channel == channel:
                if hasattr(i.shape, "center"):
                    i.shape.update_needle(float(percentage))

    def toggle_true_false(self, value):
        if value == "On":
            return True
        else:
            return False

    def create_selections(self, frame):
        # Create the selection fields for faults to be transmitted over CAN (from the Bamocar Motor Controller)
        Label(frame, text="Fault Toggles:", bg="red").grid(row=0, column=0)
        Label(frame, text="Parameter Error").grid(row=1, column=0)
        self.param_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="param_f")
        self.param_fault.set("Off")
        self.param_fault.grid(row=1, column=1)

        Label(frame, text="Output Error").grid(row=2, column=0)
        self.output_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="output_f")
        self.output_fault.set("Off")
        self.output_fault.grid(row=2, column=1)

        Label(frame, text="Safety Circuit Error").grid(row=3, column=0)
        self.safety_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="safety_f")
        self.safety_fault.set("Off")
        self.safety_fault.grid(row=3, column=1)

        Label(frame, text="Bus Transfer Error").grid(row=4, column=0)
        self.bus_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="bus_f")
        self.bus_fault.set("Off")
        self.bus_fault.grid(row=4, column=1)

        Label(frame, text="Faulty Encoder Signal").grid(row=5, column=0)
        self.feedback_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="feedback_f")
        self.feedback_fault.set("Off")
        self.feedback_fault.grid(row=5, column=1)

        Label(frame, text="No Power Supply Voltage").grid(row=6, column=0)
        self.power_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="power_f")
        self.power_fault.set("Off")
        self.power_fault.grid(row=6, column=1)

        Label(frame, text="Motor Temperature Critical").grid(row=7, column=0)
        self.mtemp_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="mtemp_f")
        self.mtemp_fault.set("Off")
        self.mtemp_fault.grid(row=7, column=1)

        Label(frame, text="Device Temperature Critical").grid(row=8, column=0)
        self.dtemp_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="dtemp_f")
        self.dtemp_fault.set("Off")
        self.dtemp_fault.grid(row=8, column=1)

        Label(frame, text="Over Voltage").grid(row=9, column=0)
        self.voltage_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="voltage_f")
        self.voltage_fault.set("Off")
        self.voltage_fault.grid(row=9, column=1)

        Label(frame, text="Over Current").grid(row=10, column=0)
        self.current_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="current_f")
        self.current_fault.set("Off")
        self.current_fault.grid(row=10, column=1)

        Label(frame, text="Racing Error").grid(row=11, column=0)
        self.raceaway_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="raceaway_f")
        self.raceaway_fault.set("Off")
        self.raceaway_fault.grid(row=11, column=1)

        Label(frame, text="User Defined Error").grid(row=12, column=0)
        self.user_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="user_f")
        self.user_fault.set("Off")
        self.user_fault.grid(row=12, column=1)

        Label(frame, text="Software Error").grid(row=13, column=0)
        self.cpu_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="cpu_f")
        self.cpu_fault.set("Off")
        self.cpu_fault.grid(row=13, column=1)

        Label(frame, text="Ballast Circuitry Overload").grid(row=14, column=0)
        self.ballast_fault = ttk.Combobox(
            frame, values=["On", "Off"], name="ballast_f")
        self.ballast_fault.set("Off")
        self.ballast_fault.grid(row=14, column=1)

        # Create a gap between faults and warnings
        Label(frame, text="").grid(row=15, column=0)
        Label(frame, text="Warning Toggles:", bg="orange").grid(row=16, column=0)
        Label(frame, text="Low/No Voltage Warning").grid(row=17, column=0)
        self.power_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="power_w")
        self.power_warning.set("Off")
        self.power_warning.grid(row=17, column=1)

        Label(frame, text="High Motor Temperature").grid(row=18, column=0)
        self.mtemp_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="mtemp_w")
        self.mtemp_warning.set("Off")
        self.mtemp_warning.grid(row=18, column=1)

        Label(frame, text="High Device Temperature").grid(row=19, column=0)
        self.dtemp_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="dtemp_w")
        self.dtemp_warning.set("Off")
        self.dtemp_warning.grid(row=19, column=1)

        Label(frame, text="Over Voltage").grid(row=20, column=0)
        self.voltage_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="voltage_w")
        self.voltage_warning.set("Off")
        self.voltage_warning.grid(row=20, column=1)

        Label(frame, text="Over Current").grid(row=21, column=0)
        self.current_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="current_w")
        self.current_warning.set("Off")
        self.current_warning.grid(row=21, column=1)

        Label(frame, text="Over Load > 87%").grid(row=22, column=0)
        self.overload_warning = ttk.Combobox(
            frame, values=["On", "Off"], name="overload_w")
        self.overload_warning.set("Off")
        self.overload_warning.grid(row=22, column=1)

        self.all_comboboxes = [
            self.param_fault, self.output_fault, self.safety_fault, self.bus_fault,
            self.feedback_fault, self.power_fault, self.mtemp_fault, self.dtemp_fault,
            self.voltage_fault, self.current_fault, self.raceaway_fault, self.user_fault,
            self.cpu_fault, self.ballast_fault, self.power_warning, self.mtemp_warning,
            self.dtemp_warning, self.voltage_warning, self.current_warning,
            self.overload_warning
        ]
        for combobox in self.all_comboboxes:
            combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

        


    def on_combobox_selected(self, event):
        # detect when a combobox has had a value change and sent message over CAN
        for combobox in self.all_comboboxes:
            selected_value = self.toggle_true_false(combobox.get())
            combobox_name = combobox.winfo_name()
            code = None
            check_against = None
            match combobox_name:
                case "param_f":
                    code = 0x00
                case "output_f":
                    code = 0x01
                case "safety_f":
                    code = 0x02
                case "bus_f":
                    code = 0x03
                case "feedback_f":
                    code = 0x04
                case "power_f":
                    code = 0x05
                    check_against = 0x15
                case "mtemp_f":
                    code = 0x06
                    check_against = 0x16
                case "dtemp_f":
                    code = 0x07
                    check_against = 0x17
                case "voltage_f":
                    code = 0x08
                    check_against = 0x18
                case "current_f":
                    code = 0x09
                    check_against = 0x19
                case "raceaway_f":
                    code = 0x0A
                case "user_f":
                    code = 0x0B
                case "cpu_f":
                    code = 0x0E
                case "ballast_f":
                    code = 0x0F
                case "power_w":
                    code = 0x15
                case "mtemp_w":
                    code = 0x16
                case "dtemp_w":
                    code = 0x17
                case "voltage_w":
                    code = 0x18
                case "current_w":
                    code = 0x19
                case "overload_w":
                    code = 0x1C
                case _:
                    code = 0xFF
            if code != None:
                if selected_value and code not in self.can_message_data:
                    self.can_message_data.append(code)
                elif not selected_value and code in self.can_message_data:
                    self.can_message_data.remove(code)
                if check_against != None and check_against in self.can_message_data:
                    self.can_message_data.remove(check_against)
        self.send_can_message()

    def send_can_message(self):
        with can.interface.Bus(interface="virtual", channel=0) as bus:
            msg = can.Message(
                arbitration_id=0x8F,
                data=self.can_message_data
            )
            try:
                bus.send(msg)
            except can.CanError:
                print("A CAN error occured!")
