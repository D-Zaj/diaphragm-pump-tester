from time import strftime
from time import time

class Logger:

    def __init__(self, filename):
        self.filename = filename


    def write (self, input, msg):
        write_str = strftime("%m/%d/%Y,%H:%M:%S") + ","
        write_str = write_str + msg + ","

        for i in range(len(input)):
            if (i == len(input) - 1):
                write_str = write_str + str(input[i])
            else:
                write_str = write_str + str(input[i]) + ","
        before_open = time()
        with open(self.filename, "a") as log_file:
            print("Time taken to open: {}".format(time() - before_open))
            log_file.write(write_str + "\n")

