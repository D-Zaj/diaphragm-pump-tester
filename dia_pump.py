import RPi.GPIO as IO
import time

class Pump_Control:
    
    def __init__( self ):
        IO.setwarnings(False)
        IO.setmode(IO.BCM)

        # Pin Definitions
        self.PUMP_PINS = [18, 19, 20, 21, 22]
        self.TACH_PINS = [4, 5, 6, 7, 8]

        # Other variables
        self.NUM_CYCLES = 20
        self.logger_flag = False
        self.stop = False

        # GPIO Pin Setup
        for pin in self.PUMP_PINS:
            IO.setup(pin, IO.OUT)
        
        for pin in self.TACH_PINS:
            IO.setup(pin, IO.IN)

        # GPIO Pin Initializations
        for pin in self.PUMP_PINS:
            IO.output(pin, IO.HIGH)
        
    def run( self ):
        for pin in self.PUMP_PINS:
            IO.output(pin, IO.LOW)

    def stop(self):
        for pin in self.PUMP_PINS:
            IO.output(pin, IO.HIGH)
    
    def get_freq(self):
        freq = []
        for i in range(5):
            count = 0
            start_time = time.time()
            while (count < self.NUM_CYCLES):
                flag = IO.wait_for_edge(self.TACH_PINS[i], IO.FALLING, timeout=1000)
                if flag is None:
                    freq[i] = 0
                    break
                count += 1
            time_elapsed = time.time() - start_time
            freq[i] = self.NUM_CYCLES / time_elapsed
        return freq