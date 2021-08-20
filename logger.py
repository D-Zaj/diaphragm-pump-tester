from time import strftime

class Logger:

    def __init__(self):
        pass

    def open (self, filename):

        self.log_file = open(filename, "a")
        self._fileopen = True

    def write (self, input, msg):
        write_str = strftime("%m/%d/%Y,%H:%M:%S") + ","
        write_str = write_str + msg + ","

        for i in range(len(input)):
            if (i == len(input) - 1):
                write_str = write_str + str(input[i])
            else:
                write_str = write_str + str(input[i]) + ","

        self.log_file.write(write_str + "\n")

    def close (self):

        self.log_file.close()
        self._fileopen = False

    def get_status (self):

        return self._fileopen

