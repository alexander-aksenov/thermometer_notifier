class Logger:
    def __init__(self, log_file, data_storage):
        # TODO: move to a separate static?
        self.__file = open(log_file, 'a')
        self.__ds = data_storage

    def write(self):
        time = self.__ds.time
        temperature = "%.1f" % self.__ds.temperature
        humidity = "%.1f" % self.__ds.humidity
        write_str = str(time) + ": " + str(temperature) + "° " + str(humidity) + "%\n"
        self.__file.write(write_str)
        self.__file.flush()

    def close(self):
        self.__file.close()
