from tkinter import *
import tkinter.ttk as ttk

class MainGUI:

    def __init__(self, window):

        self.run_callback = None
        self.freq_callback = None

        # Create root window
        window.title("Diaphragm Pump Tester")
        window.iconbitmap(default="transparent.ico")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        # Create main frame to fill window (this is done for consistency in appearance)
        mainframe = ttk.Frame(window)

        ### Create first major frame for test settings ###
        Control_Frame = ttk.Frame(mainframe)

        # Create duty cycle setting
        self.Duty_cycle = IntVar()
        duty_cycle_frame = ttk.Frame(Control_Frame, padding="10 5")
        dc_label = ttk.Label(duty_cycle_frame, text="Select duty cycle: ")
        dc_entry = ttk.Combobox(duty_cycle_frame, width=4, textvariable=self.Duty_cycle, values=("10", "20", "30", "40", "50", "60", "70", "80", "90", "100"))
        dc_units = ttk.Label(duty_cycle_frame, text="%")
        dc_spacer = ttk.Frame(duty_cycle_frame)

        # Pack widgets into duty_cycle_frame
        dc_label.pack(side=LEFT)
        dc_spacer.pack(side=LEFT)
        dc_units.pack(side=RIGHT)
        dc_entry.pack(side=RIGHT)

        # Create frame and widgets for run time setting
        run_time_frame = ttk.Frame(Control_Frame, padding="10 5")
        rt_label = ttk.Label(run_time_frame, text="Enter desired run time \n(Enter 0 to run indefinitely): ")
        rt_entry = ttk.Entry(run_time_frame, width=6)
        self.Run_time = StringVar()
        rt_units = ttk.Combobox(run_time_frame, values=("sec", "min", "hr", "days"), width=4, textvariable=self.Run_time)
        rt_units.set("sec") # Set default unit
        rt_units.state(['readonly']) # Set dropdown menu to read only
        # Pack rt widgets into run_time_frame
        rt_label.pack(side=LEFT)
        rt_entry.pack(side=LEFT)
        rt_units.pack(side=LEFT)

        # Pack elements into Control_Frame using a grid layout
        duty_cycle_frame.grid(column=0, row=0, sticky="w")
        run_time_frame.grid(column=0, row=1, sticky="w")

        ### Create major frame for logger settings ###
        Logger_Frame = ttk.Frame(mainframe)

        # Checkbox to select whether program should log frequency readings
        log_checkbox_frame = ttk.Frame(Logger_Frame, padding="10 5")
        self.logger_flag = IntVar()
        log_box = ttk.Checkbutton(log_checkbox_frame, text="Log Readings", variable=self.logger_flag, command=self.check_handler)
        log_box.pack(side=RIGHT)

        # Interval entry to specify time between readings
        self.interval = StringVar()
        interval_frame = ttk.Frame(Logger_Frame, padding="10 5")
        int_label = ttk.Label(interval_frame, text="Interval: ")
        self.int_entry = ttk.Entry(interval_frame, textvariable=self.interval)
        int_unit = ttk.Label(interval_frame, text="s")
        # Pack elements together into interval_frame
        int_label.pack(side=LEFT)
        self.int_entry.pack(side=LEFT)
        int_unit.pack(side=LEFT)

        # File path entry to specify where to save logged data
        self.File_path = StringVar()
        file_path_frame = ttk.Frame(Logger_Frame, padding="10 5")
        fp_label = ttk.Label(file_path_frame, text="File path: ")
        self.fp_entry = ttk.Entry(file_path_frame, textvariable=self.File_path)
        # Pack elements into file_path_frame
        fp_label.pack(side=LEFT)
        self.fp_entry.pack(side=LEFT)

        # File name entry to specify file name of logged data
        self.File_name = StringVar()
        file_name_frame = ttk.Frame(Logger_Frame, padding="10 5")
        fn_label = ttk.Label(file_name_frame, text="Export as: ")
        self.fn_entry = ttk.Entry(file_name_frame, textvariable=self.File_name)
        # Pack elements into file_name_frame
        fn_label.pack(side=LEFT)
        self.fn_entry.pack(side=LEFT)

        # Disable all logger related items by default
        self.int_entry.state(['disabled'])
        self.fp_entry.state(['disabled'])
        self.fn_entry.state(['disabled'])

        # Pack sub elements into major frame Logger_Frame
        log_checkbox_frame.grid(column=0, row=0)
        interval_frame.grid(column=0, row=1)
        file_path_frame.grid(column=0, row=2)
        file_name_frame.grid(column=0, row=3)

        ### Create major frame for run buttons ###
        Run_Frame = ttk.Frame(mainframe)

        #Create run button
        run_button = ttk.Button(Run_Frame, text="Run Test", command=self.run_handler)
        #Create button to get current frequency
        freq_button = ttk.Button(Run_Frame, text="Get frequency", command=self.freq_handler)

        run_button.grid(column=0, row=0)
        freq_button.grid(column=1, row=0)
        
        # Populate main window grid with major frames
        Control_Frame.grid(column=0, row=0, padx=10, pady=10)
        Logger_Frame.grid(column=1, row=0, padx=10, pady=10)
        Run_Frame.grid(column=0, columnspan=1, row=1)
        mainframe.grid(column=0, row=0)

    # Enables or disables logger related entries based on checkbox status
    def check_handler(self):
        if self.logger_flag.get():
            self.int_entry.state(['!disabled'])
            self.fp_entry.state(['!disabled'])
            self.fn_entry.state(['!disabled'])
        else:
            self.int_entry.state(['disabled'])
            self.fp_entry.state(['disabled'])
            self.fn_entry.state(['disabled'])

    def run_handler(self):
        if self.run_callback is not None:
            self.run_callback()
        else:
            print("Testing run button")
    def set_run_handler(self, fn):
        self.run_callback = fn

    def freq_handler(self):
        if self.run_callback is not None:
            self.freq_callback()
        else:
            print("Testing freq handler")
    
    def set_freq_handler(self, fn):
        self.freq_callback = fn

    def get_duty_cycle(self):
        return self.Duty_cycle
    
    def get_run_time(self):
        return self.Run_time
    
    def get_interval(self):
        return self.interval

    def get_file_path(self):
        return self.File_path

    def get_file_name(self):
        return self.File_name
