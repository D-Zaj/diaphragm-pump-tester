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
        self.duty_cycle = 100 # Initialize duty cycle at 100% (which means pump is off)
        self.logger_flag = False
        self.stop = False

        # GPIO Pin Setup
        IO.setup(PWM_PIN, IO.OUT)
        IO.setup(TACH_PIN, IO.IN)
        self.p = IO.PWM(PWM_PIN, PWM_FREQ)

        # GPIO Pin Initializations
        self.p.start(self.duty_cycle)
        
    def run_pump(self, duty_cycle=0, run_time=0):
        start_time = time.time()
        current_time = time.time()
        if (run_time > 0):
            while(not self.stop and (current_time - start_time < run_time)):
                
                # Do stuff, run pump,
        else:
            self.p.ChangeDutyCycle(duty_cycle)
    
    def stop(self):
        self.stop = True
        