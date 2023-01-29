import pigpio
import time
from thermometer import Thermometer



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


pi = pigpio.pi()
if pi.connected:
    print('pi connected')
    pi.set_mode(red_gpio, pigpio.INPUT)
    pi.set_mode(yellow_gpio, pigpio.INPUT)
    pi.set_mode(green_gpio, pigpio.INPUT)

    thermometer = Thermometer(therm_gpio, pi)
    thermometer.start()

    i = 0
    while(i < 1000):
        thermometer.trigger()
        time.sleep(3)
        hum = thermometer.humidity
        temp = thermometer.temperature
        print(str(temp) + " - " + str(hum))
        if temp >= red_threshold:
            red_light_on(pi)
        elif temp >= yellow_threshold:
            yellow_light_on(pi)
        else:
            green_light_on(pi)
    thermometer.stop()
pi.stop()

