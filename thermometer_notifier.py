import pigpio
import time
import os
from threading import Thread
from data_storage import DataStorage
from thermometer import Thermometer
from logger import Logger
from tgbot import TgBot
from plotter import Plotter
import config


TOKEN = os.getenv('TOKEN')

def red_light_on(pi):
    pi.write(config.RED_LIGHT_GPIO, pigpio.HIGH)
    pi.write(config.YELLOW_LIGHT_GPIO, pigpio.LOW)
    pi.write(config.GREEN_LIGHT_GPIO, pigpio.LOW)

def yellow_light_on(pi):
    pi.write(config.YELLOW_LIGHT_GPIO, pigpio.HIGH)
    pi.write(config.RED_LIGHT_GPIO, pigpio.LOW)
    pi.write(config.GREEN_LIGHT_GPIO, pigpio.LOW)

def green_light_on(pi):
    pi.write(config.GREEN_LIGHT_GPIO, pigpio.HIGH)
    pi.write(config.YELLOW_LIGHT_GPIO, pigpio.LOW)
    pi.write(config.RED_LIGHT_GPIO, pigpio.LOW)

def all_lights_off(pi):
    pi.write(config.GREEN_LIGHT_GPIO, pigpio.LOW)
    pi.write(config.YELLOW_LIGHT_GPIO, pigpio.LOW)
    pi.write(config.RED_LIGHT_GPIO, pigpio.LOW)

def check_temp_is_green(temp):
    if temp >= config.GREEN_ZONE[0] and temp <= config.GREEN_ZONE[1]:
        return True
    return False

def check_temp_is_yellow(temp):
    if temp >= config.YELLOW_ZONE[0] and temp <= config.YELLOW_ZONE[1]:
        return True
    return False

def data_read_iter(thermometer, logger, data_storage, pi, tgbot):
    print("Trigger thermomether")
    thermometer.trigger()
    time.sleep(config.ITER_DELAY_TIME)
    print("Write log")
    logger.write()
    temp = data_storage.temperature
    temp_out = "%.1f" % data_storage.temperature
    hum_out = "%.1f" % data_storage.humidity
    time_out = data_storage.time
    print(str(time_out) + ": " + str(temp_out) + "° " + str(hum_out) + "%")
    if check_temp_is_green(temp):
        green_light_on(pi)
    elif check_temp_is_yellow(temp):
        print("Send notification")
        tgbot.send_temperature()
        yellow_light_on(pi)
    else:
        print("Send notification")
        tgbot.send_temperature()
        red_light_on(pi)

def read_thread(thermometer, logger, data_storage, pi, tgbot):
    while(True):
        data_read_iter(thermometer, logger, data_storage, pi, tgbot)


pi = pigpio.pi()
if pi.connected:
    print('pi connected')
    pi.set_mode(config.RED_LIGHT_GPIO, pigpio.INPUT)
    pi.set_mode(config.YELLOW_LIGHT_GPIO, pigpio.INPUT)
    pi.set_mode(config.GREEN_LIGHT_GPIO, pigpio.INPUT)

    data_storage = DataStorage()
    logger = Logger(config.LOG_FILE, data_storage)

    thermometer = Thermometer(config.THERMOMETER_GPIO, pi, data_storage)
    thermometer.start()

    plotter = Plotter(config.LOG_FILE, config.GREEN_ZONE, config.YELLOW_ZONE, config.IMAGE_FILE)

    tgbot = TgBot.create(TOKEN, data_storage, plotter)

    read_th = Thread(target=read_thread, args=(thermometer, logger, data_storage, pi, tgbot))
    read_th.start()

    tgbot.run()

    thermometer.stop()
    read_th.join()
    all_lights_off(pi)
    logger.close()
pi.stop()

