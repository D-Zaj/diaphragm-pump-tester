import RPi.GPIO as IO
import time

class Pump_Control:
    
    def __init__( self ):
        
        IO.setwarnings(False)
        IO.setmode(IO.BCM)

        # Pin Definitions
        self.PUMP_PINS = [17, 23, 10, 5, 16]
        self.TACH_PINS = [18, 24, 25, 6, 19]

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
            IO.output(pin, IO.HIGH) # Set all pump ctrl pins high so pumps are initially off
    
    def run_all( self ):
        for pin in self.PUMP_PINS:
            IO.output(pin, IO.LOW)

    def stop_all( self ):
        for pin in self.PUMP_PINS:
            IO.output(pin, IO.HIGH)
    
    def get_freq( self ):
        freq = []
        for pin in self.TACH_PINS:
            pump_off = False
            count = 0
            start_time = time.time()
            while (count < self.NUM_CYCLES):
                flag = IO.wait_for_edge(pin, IO.FALLING, timeout=1000)
                if flag is None:
                    pump_off = True
                    break
                count += 1
            
            if pump_off:
                freq.append(0)
            else:
                time_elapsed = time.time() - start_time
                freq.append(self.NUM_CYCLES / time_elapsed)
        return freq
