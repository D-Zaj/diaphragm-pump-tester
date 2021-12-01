from tkinter import *
import tkinter
import tkinter.ttk as ttk
import math
import time
from datetime import timedelta
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

        self.Run_time = StringVar()
        self.rt_unit = StringVar()
        self.rt = 0

        self.timer_interval = 5 * self.time_units["min"]

        # Log related vars
        self.FILE_PATH = "tach_log.csv"
        self.STOP_MSG = "Stopped pumps"
        self.RUN_MSG = "Started pumps"
        self.NO_INPUT = ["---","---","---","---","---"]
        self.LOG_INTERVAL = 10 * self.time_units["min"] # Defines automatic logging interval
        self.is_running = False

        """Initialize Logging"""
        self.logger = Logger(self.FILE_PATH)

        # Create root window
        self.title( "Diaphragm Pump Tester" )
        # self.iconbitmap( default="transparent.ico" )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create main frame to fill window (this is done for consistency in appearance)
        self.mainframe = ttk.Frame(self, padding="5")

        """ Create first major frame for test settings  """
        self.Control_Frame = ttk.Frame(self.mainframe)

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
        if self.run_callback is not None and self.is_running is not True:
            self.run_callback()
            self.is_running = True
            self.rt = int( self.Run_time.get() )
            unit = self.rt_unit.get()
            self.rt = self.rt * self.time_units[unit]
            if  self.rt > 0:
                self.init_time = time.monotonic()
                self.after( self.rt * 1000, self.stop_handler )
                self.timer()

            self.logger.write(self.NO_INPUT, self.RUN_MSG)
            self.after( self.LOG_INTERVAL * 1000, self.auto_log )
        else:
            print("Testing run button")
            print("Run time = %d" % (int(self.Run_time.get()) * 1000 * self.time_units[self.rt_unit.get()]) )

    def set_freq_callback( self, fn ):
        self.freq_callback = fn
    
    def freq_handler( self ):
        if self.DEBUG: print("Getting pump frequency...")
        if self.freq_callback is not None and self.is_running:
            freq = self.freq_callback()
            self.logger.write(freq, "Manual freq log")
            if self.DEBUG: print(f"Pump 1: {freq[0]}, Pump 2: {freq[1]}, Pump 3: {freq[2]}, Pump 4: {freq[3]}, Pump 5: {freq[4]}")
        else:
            print("Error, freq callback not set or pumps not running")
        if self.DEBUG: print("Done.")

    def auto_log( self ):
        if self.freq_callback is not None and self.is_running:
            if self.DEBUG: print("Getting pump frequencies...")
            freq = self.freq_callback()
            if self.DEBUG: print("Done.")
            
            self.logger.write(freq, "Automatic freq log")
            self.after( self.LOG_INTERVAL * 1000, self.auto_log )
    
    def set_stop_callback( self, fn ):
        self.stop_btn_callback = fn

    def stop_handler( self ):
        if self.stop_btn_callback is not None and self.is_running:
            self.stop_btn_callback()
            self.logger.write(self.NO_INPUT, self.STOP_MSG)
            self.is_running = False
        else:
            print("Testing stop button")

    def timer( self ):
        
        # hour = math.floor(time / self.time_units["hr"])
        # minute = math.floor((time - hour * self.time_units["hr"]) / 60)
        # sec = time - hour * self.time_units["hr"] - minute * self.time_units["min"]
        # print(f"Time elapsed: {hour:02d}:{minute:02d}:{sec:02d} of {total_hour:d} hours")

        # if self.is_running and (time-self.timer_interval < self.rt):
        #     self.after(self.timer_interval * 1000, self.timer, time + self.timer_interval)
        
        total_time = time.gmtime(self.rt)
        total_time = time.strftime("%H:%M:%S", total_time)
        
        current_time = time.monotonic()
        delta = current_time - self.init_time   # in seconds
        elapsed = time.gmtime(delta)
        elapsed = time.strftime("%H:%M:%S", elapsed)
        print(f"Time elapsed: {elapsed} of {total_time}")
        
        if delta + self.timer_interval < self.rt and self.is_running:
            self.after(self.timer_interval * 1000, self.timer)
