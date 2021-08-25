from time import strftime

class Logger:

    def __init__(self, filename):
        self.filename = filename
        header = "Date,Time,Message,Pump 1 Tach,Pump 2 Tach,Pump 3 Tach,Pump 4 Tach,Pump 5 Tach"

    def write (self, input, msg):
        write_str = strftime("%m/%d/%Y,%H:%M:%S") + ","
        write_str = write_str + msg + ","

        for i in range(len(input)):
            if (i == len(input) - 1):
                write_str = write_str + str(input[i])
            else:
                write_str = write_str + str(input[i]) + ","
        
        with open(self.filename, "a") as log_file:
            log_file.write(write_str + "\n")

