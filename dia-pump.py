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
        
    

        