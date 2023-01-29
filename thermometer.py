import pigpio
import time

class Thermometer:
    def __init__(self, gpio, pi):
        self.__gpio = gpio
        self.__pi = pi
        self.__high_tick = 0
        self.__bit = 40
        self.__bad_MM = 0
        self.__bad_CS = 0
        self.__no_response = 0
        self.__hH = 0
        self.__hL = 0
        self.__tH = 0
        self.__tL = 0
        self.__CS = 0
        self.__rhum = -999
        self.__temp = -999
        self.__cb = None

    def _cb(self, gpio, level, tick):
        diff = pigpio.tickDiff(self.__high_tick, tick)
        if level == 0:
            if diff >= 50:
                val = 1
                if diff > 199:
                    self.__CS = 256
            else:
                val = 0
            if self.__bit >= 40:
                self.__bit = 40
            elif self.__bit >= 32:
                self.__CS = (self.__CS << 1) + val
                if self.__bit == 39:
                    self.__pi.set_watchdog(gpio, 0)
                    self.__no_response = 0
                    total = self.__hH + self.__hL + self.__tH + self.__tL
                    if (total & 255) == self.__CS:
                        self.__rhum = ((self.__hH << 8) + self.__hL) * 0.1
                        if self.__tH & 128:
                            mult = -0.1
                            self.__tH = self.__tH & 127
                        else:
                            mult = 0.1
                        self.__temp = ((self.__tH << 8) + self.__tL) * mult
                    else:
                        self.__bad_CS += 1
            elif self.__bit >= 24:
                self.__tL = (self.__tL << 1) + val
            elif self.__bit >= 16:
                self.__tH = (self.__tH << 1) + val
            elif self.__bit >= 8:
                self.__hL = (self.__hL << 1) + val
            elif self.__bit >= 0:
                self.__hH = (self.__hH << 1) + val
            else:
                pass
            self.__bit += 1
        elif level == 1:
            self.__high_tick = tick
            if diff > 250000:
                self.__bit = -2
                self.__hH = 0
                self.__hL = 0
                self.__tH = 0
                self.__tL = 0
                self.__CS = 0
        else: # timeout
            self.__pi.set_watchdog(gpio, 0)
            if self.__bit < 8:
                self.__bad_MM += 1
                self.__no_response += 1
                print("No response!")
            elif bit < 39:
                self.__bad_MM += 1
                self.__no_response = 0
                print("Short message!")
            else:
                self.__no_response = 0

    def trigger(self):
        self.__pi.write(self.__gpio, pigpio.LOW)
        time.sleep(0.017)
        self.__pi.set_mode(self.__gpio, pigpio.INPUT)
        self.__pi.set_watchdog(self.__gpio, 200)

    def start(self):
        self.__pi.set_pull_up_down(self.__gpio, pigpio.PUD_OFF)
        self.__pi.set_watchdog(self.__gpio, 0)  # Kill any watchdogs.
        cb = self.__pi.callback(self.__gpio, pigpio.EITHER_EDGE, self._cb)

    def stop(self):
        self.__pi.set_watchdog(gpio, 0)
        if self.__cb:
            self.__cb.cancel()
            self.__cb = None

    @property
    def temperature(self):
        return self.__temp

    @property
    def humidity(self):
        return self.__rhum
