import pigpio
import time
from data_storage import DataStorage
from thermometer import Thermometer
from logger import Logger


log_file = "temp.log"

therm_gpio = 4

red_gpio = 22
green_gpio = 24
yellow_gpio = 23

red_threshold = 21
yellow_threshold = 19

def red_light_on(pi):
    pi.write(red_gpio, pigpio.HIGH)
    pi.write(yellow_gpio, pigpio.LOW)
    pi.write(green_gpio, pigpio.LOW)

def yellow_light_on(pi):
    pi.write(yellow_gpio, pigpio.HIGH)
    pi.write(red_gpio, pigpio.LOW)
    pi.write(green_gpio, pigpio.LOW)

def green_light_on(pi):
    pi.write(green_gpio, pigpio.HIGH)
    pi.write(yellow_gpio, pigpio.LOW)
    pi.write(red_gpio, pigpio.LOW)

def all_lights_off(pi):
    pi.write(green_gpio, pigpio.LOW)
    pi.write(yellow_gpio, pigpio.LOW)
    pi.write(red_gpio, pigpio.LOW)


pi = pigpio.pi()
if pi.connected:
    print('pi connected')
    pi.set_mode(red_gpio, pigpio.INPUT)
    pi.set_mode(yellow_gpio, pigpio.INPUT)
    pi.set_mode(green_gpio, pigpio.INPUT)

    data_storage = DataStorage()
    logger = Logger(log_file, data_storage)

    thermometer = Thermometer(therm_gpio, pi, data_storage)
    thermometer.start()

    i = 0
    while(i < 50):
        thermometer.trigger()
        time.sleep(3)
        logger.write()
        temp = data_storage.temperature
        temp_out = "%.1f" % data_storage.temperature
        hum_out = "%.1f" % data_storage.humidity
        time_out = data_storage.time
        print(str(time_out) + ": " + str(temp_out) + "° " + str(hum_out) + "%")
        if temp >= red_threshold:
            red_light_on(pi)
        elif temp >= yellow_threshold:
            yellow_light_on(pi)
        else:
            green_light_on(pi)
        i += 1
    thermometer.stop()
    all_lights_off(pi)
    logger.close()
pi.stop()

