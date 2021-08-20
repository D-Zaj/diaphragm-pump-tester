import tkinter as tk
import threading
from gui import MainGUI
import random
# from dia_pump import Pump_Control

def freq_test():
    return random.randint(0, 100)

if __name__ == '__main__':
    window = tk.Tk()
    gui = MainGUI( window )
    # pump = Pump_Control()

    """gui.set_freq_callback( pump.get_freq )
    gui.set_run_callback( pump.run )
    gui.set_stop_callback( pump.stop )"""
    gui.set_freq_callback( freq_test )

    gui_thread = threading.Thread( target=window.mainloop() )
    gui_thread.start()


