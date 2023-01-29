class DataStorage:
    def __init__(self):
        self.__temp = -999
        self.__hum = -999

    @property
    def temperature(self):
        return self.__temp

    @temperature.setter
    def temperature(self, t):
        self.__temp = t

    @property
    def humidity(self):
        return self.__hum

    @humidity.setter
    def humidity(self, h):
        self.__hum = h

