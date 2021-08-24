from tkinter import *
import tkinter
import tkinter.ttk as ttk
from logger import Logger

class MainGUI(tkinter.Tk):

    def __init__( self ):
        print("Starting maingui init")
        super().__init__()
        print("Initialized root")
        # Various variables
        self.run_callback = None
        self.freq_callback = None
        self.stop_btn_callback = None
        self.time_units = {"sec" : 1, "min" : 60, "hr" : 3600, "days" : 86400}
        self.DEBUG = True

        self.Duty_cycle = IntVar()
        self.Run_time = StringVar()
        self.rt_unit = StringVar()

        # Log related vars
        self.FILE_PATH = "tach_log.csv"
        self.STOP_MSG = "Stopped pumps."
        self.RUN_MSG = "Started pumps."
        self.NO_INPUT = ["---","---","---","---","---"]
        self.LOG_INTERVAL = 2000
        self.is_running = False


        """Initialize Logging"""
        self.logger = Logger()
        if self.DEBUG: print(self.logger.get_status)
        self.logger.open(self.FILE_PATH)
        if self.DEBUG: print(self.logger.get_status)
        if self.DEBUG: print("Opened tach log")
        self.logger.write(self.NO_INPUT,"Opened log file.")


        # Create root window
        self.title( "Diaphragm Pump Tester" )
        self.iconbitmap( default="transparent.ico" )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create main frame to fill window (this is done for consistency in appearance)
        self.mainframe = ttk.Frame(self, padding="5")

        """ Create first major frame for test settings  """
        self.Control_Frame = ttk.Frame(self.mainframe)

        # Create duty cycle setting
        duty_cycle_frame = ttk.Frame(self.Control_Frame, padding="10 5")
        dc_label = ttk.Label(duty_cycle_frame, text="Select duty cycle: ")
        dc_entry = ttk.Combobox(duty_cycle_frame, width=4, textvariable=self.Duty_cycle, values=("10", "20", "30", "40", "50", "60", "70", "80", "90", "100"))
        dc_entry.set("10")
        dc_units = ttk.Label(duty_cycle_frame, text="%")
        dc_spacer = ttk.Frame(duty_cycle_frame)

        # Pack widgets into duty_cycle_frame
        dc_label.pack(side=LEFT)
        dc_spacer.pack(side=LEFT)
        dc_units.pack(side=RIGHT)
        dc_entry.pack(side=RIGHT)

        # Create frame and widgets for run time setting
        run_time_frame = ttk.Frame(self.Control_Frame, padding="10 5")
        rt_label = ttk.Label(run_time_frame, text="Enter desired run time \n(Enter 0 to run indefinitely): ")
        rt_entry = ttk.Entry(run_time_frame, width=6, textvariable=self.Run_time)
        rt_units = ttk.Combobox(run_time_frame, values=("sec", "min", "hr", "days"), width=4, textvariable=self.rt_unit)
        self.Run_time.set("0")
        rt_units.set("hr") # Set default unit
        rt_units.state(['readonly']) # Set dropdown menu to read only
        # Pack rt widgets into run_time_frame
        rt_label.pack(side=LEFT)
        rt_entry.pack(side=LEFT)
        rt_units.pack(side=LEFT)

        # Pack elements into self.Control_Frame using a grid layout
        # duty_cycle_frame.grid(column=0, row=0, sticky="w")
        run_time_frame.grid(column=0, row=1, sticky="w")

        """ Create major frame for run buttons """ 
        Run_Frame = ttk.Frame(self.mainframe)

        #Create run button
        run_button = ttk.Button(Run_Frame, text="Start Pumps", command=self.run_handler)
        #Create button to get current frequency
        freq_button = ttk.Button(Run_Frame, text="Log Current Frequency", command=self.freq_handler)
        #Create button to stop pump
        stop_button = ttk.Button(Run_Frame, text="Stop Pumps", command=self.stop_handler)
        btn_spacer = ttk.Frame(Run_Frame, width=25)

        run_button.grid(column=0, row=0)
        stop_button.grid(column=1, row=0)
        btn_spacer.grid(column=2, row=0)
        freq_button.grid(column=3, row=0)
        
        # Populate main window grid with major frames
        self.Control_Frame.grid(column=0, row=0, padx=10, pady=10)
        Run_Frame.grid(column=0, columnspan=1, row=1, padx=10)
        self.mainframe.grid(column=0, row=0)

        # This just sets the minimum window size
        self.update_idletasks()
        self.after_idle(lambda: self.minsize(self.winfo_width(), self.winfo_height()))
        if self.DEBUG: print("Finshed gui init")


    def set_run_callback( self, fn ):
        self.run_callback = fn

    def run_handler( self ):
        if self.run_callback is not None:
            rt = int( self.Run_time.get() )
            unit = self.rt_unit.get()
            if  rt > 0:
                self.run_callback()
                self.after( rt * 1000 * self.time_units[unit], self.stop_handler )
            else:
                self.run_callback()
            
            print(self.logger.get_status)
            if self.DEBUG:
                if (self.logger.get_status is not True):
                    print("It works!")
            if self.logger.get_status is not True:
                self.logger.open(self.FILE_PATH)

            self.logger.write(self.NO_INPUT, self.RUN_MSG)
            self.is_running = True
            self.after( self.LOG_INTERVAL, self.auto_log )

        else:
            print("Testing run button")
            print("Run time = %d" % (int(self.Run_time.get()) * 1000 * self.time_units[self.rt_unit.get()]) )

    def set_freq_callback( self, fn ):
        self.freq_callback = fn
    
    def freq_handler( self ):
        if self.freq_callback is not None and self.is_running:
            freq = self.freq_callback()
            self.logger.write(freq, "Manual freq log")
            print("Pump 1: {}, Pump 2: {}, Pump 3: {}, Pump 4: {}, Pump 5: {}".format(freq[0], freq[1], freq[2], freq[3], freq[4]) )
        else:
            print("Error, freq callback not set")

    def auto_log( self ):
        if self.freq_callback is not None and self.is_running:
            freq = self.freq_callback()
            self.logger.write(freq, "Automatic freq log")
            self.after( self.LOG_INTERVAL, self.auto_log )
    
    def set_stop_callback( self, fn ):
        self.stop_btn_callback = fn

    def stop_handler( self ):
        if self.stop_btn_callback is not None and self.is_running:
            self.stop_btn_callback()
            self.logger.write(self.NO_INPUT, self.STOP_MSG)
            self.logger.close()
            self.is_running = False
        else:
            print("Testing stop button")
