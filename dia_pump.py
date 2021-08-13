import RPi.GPIO as IO
import time

class Pump_Control:
    
    def __init__(self, pwm_pin, tach_pin, freq=500):
        IO.setwarnings(False)
        IO.setmode(IO.BCM)

        # Pin Definitions
        self.PWM_PIN = pwm_pin
        self.TACH_PIN = tach_pin

        # Other variables
        self.PWM_FREQ = freq
        self.NUM_CYCLES = 20
        self.logger_flag = False
        self.stop = False

        # GPIO Pin Setup
        IO.setup(self.PWM_PIN, IO.OUT)
        IO.setup(self.TACH_PIN, IO.IN)
        self.p = IO.PWM(self.PWM_PIN, self.PWM_FREQ)

        # GPIO Pin Initializations
        self.p.start(100) # Start pump at 100% duty (which is off)
        
    def run_pump(self, duty_cycle):
        self.p.ChangeDutyCycle(duty_cycle)

    def stop(self):
        self.p.ChangeDutyCycle(100)
    
    def get_freq(self):
        freq = 0
        count = 0
        start_time = time.time()
        while (count < self.NUM_CYCLES):
            flag = IO.wait_for_edge(self.TACH_PIN, IO.FALLING, timeout=1000)
            if flag is None:
                freq = 0
                break

            count += 1
        time_elapsed = time.time() - start_time
        freq = self.NUM_CYCLES / time_elapsed
        return freq