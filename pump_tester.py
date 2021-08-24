# import tkinter as tk
# import threading
from gui import MainGUI
import random
# from dia_pump import Pump_Control

def freq_test():
    freq = [0,0,0,0,0]
    for i in range(5):
        freq[i] = random.randint(0, 100)
    return freq

def stop_func():
    return

def run_func():
    return

if __name__ == '__main__':

    gui = MainGUI()
    # pump = Pump_Control()

    """gui.set_freq_callback( pump.get_freq )
    gui.set_run_callback( pump.run )
    gui.set_stop_callback( pump.stop )"""
    gui.set_freq_callback( freq_test )
    if gui.DEBUG: print("Set freq callback")
    gui.set_run_callback( run_func )
    if gui.DEBUG: print("Set run callback")
    gui.set_stop_callback( stop_func )
    if gui.DEBUG: print("Set stop callback")

    # gui_thread = threading.Thread( target=window.mainloop() )
    # gui_thread.start()
    if gui.DEBUG: print("About to start mainloop")
    gui.mainloop()


