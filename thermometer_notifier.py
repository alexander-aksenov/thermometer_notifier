import pigpio
import time




gpio = 4
high_tick = 0
bit = 40
bad_MM = 0
bad_CS = 0
no_response = 0
hH = 0
hL = 0
tH = 0
tL = 0
CS = 0
rhum = -999
temp = -999

red_gpio = 22
green_gpio = 24
yellow_gpio = 23

def red_light_on():
    pi.write(red_gpio, pigpio.HIGH)
    pi.write(yellow_gpio, pigpio.LOW)
    pi.write(green_gpio, pigpio.LOW)

def yellow_light_on():
    pi.write(yellow_gpio, pigpio.HIGH)
    pi.write(red_gpio, pigpio.LOW)
    pi.write(green_gpio, pigpio.LOW)

def green_light_on():
    pi.write(green_gpio, pigpio.HIGH)
    pi.write(yellow_gpio, pigpio.LOW)
    pi.write(red_gpio, pigpio.LOW)


def _cb(gpio, level, tick):
    global high_tick
    global bit
    global hH
    global hL
    global tH
    global tL
    global temp
    global rhum
    global CS
    global no_response
    global bad_MM
    global bad_CS


    diff = pigpio.tickDiff(high_tick, tick)
    if level == 0:
        if diff >= 50:
            val = 1
            if diff > 199:
                CS = 256
        else:
            val = 0
        if bit >= 40:
            bit = 40
        elif bit >= 32:
            CS = (CS << 1) + val
            if bit == 39:
                pi.set_watchdog(gpio, 0)
                no_response = 0
                total = hH + hL + tH + tL
                if (total & 255) == CS:
                    rhum = ((hH << 8) + hL) * 0.1
                    if tH & 128:
                        mult = -0.1
                        tH = tH & 127
                    else:
                        mult = 0.1
                    temp = ((tH << 8) + tL) * mult
                    print("Temp: " + str(temp) + " hum: " + str(rhum))
                    if temp >= 21:
                        red_light_on()
                    elif temp >= 19:
                        yellow_light_on()
                    else:
                        green_light_on()
                else:
                    bad_CS += 1
        elif bit >= 24:
            tL = (tL << 1) + val
        elif bit >= 16:
            tH = (tH << 1) + val
        elif bit >= 8:
            hL = (hL << 1) + val
        elif bit >= 0:
            hH = (hH << 1) + val
        else:
            pass
        bit += 1
    elif level == 1:
        high_tick = tick
        if diff > 250000:
            bit = -2
            hH = 0
            hL = 0
            tH = 0
            tL = 0
            CS = 0
    else: # timeout
        pi.set_watchdog(gpio, 0)
        if bit < 8:
            bad_MM += 1
            no_response += 1
            print("No response!")
        elif bit < 39:
            bad_MM += 1
            no_response = 0
            print("Short message!")
        else:
            no_response = 0

def trigger(gpio):
     pi.write(gpio, pigpio.LOW)
     time.sleep(0.017)
     pi.set_mode(gpio, pigpio.INPUT)
     pi.set_watchdog(gpio, 200)

def cancel(gpio):
     pi.set_watchdog(gpio, 0)


pi = pigpio.pi()
if pi.connected:
    print('pi connected')
    pi.set_mode(red_gpio, pigpio.INPUT)
    pi.set_mode(yellow_gpio, pigpio.INPUT)
    pi.set_mode(green_gpio, pigpio.INPUT)

    pi.set_pull_up_down(gpio, pigpio.PUD_OFF)
    pi.set_watchdog(gpio, 0)  # Kill any watchdogs.
    cb = pi.callback(gpio, pigpio.EITHER_EDGE, _cb)

    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)

    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    trigger(gpio)
    time.sleep(3)
    cancel(gpio)
    cb.cancel()
    cb = None
pi.stop()

