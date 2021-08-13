import tkinter as tk
import threading
from gui import MainGUI
# from dia_pump import Pump_Control

def freq_test():
    return 69

if __name__ == '__main__':
    window = tk.Tk()
    gui = MainGUI( window )
    # pump = Pump_Control( 4, 18 )

    """gui.set_freq_handler( pump.get_freq )
    gui.set_run_handler( pump.run_pump )
    gui.set_stop_handler( pump.stop )"""
    gui.set_freq_handler( freq_test )

    gui_thread = threading.Thread( target=window.mainloop() )
    gui_thread.start()


