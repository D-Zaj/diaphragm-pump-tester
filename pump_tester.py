import tkinter as tk
import threading
from gui import MainGUI

if __name__ == '__main__':
    window = tk.Tk()
    gui = MainGUI(window)
    gui_thread = threading.Thread(target=window.mainloop())
    gui_thread.start()