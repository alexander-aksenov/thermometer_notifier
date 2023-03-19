# Config for thermometer_notifier

# Temperature zones - tuples where first number is lower bound, second - high bound
GREEN_ZONE=(15, 19)
YELLOW_ZONE=(12, 21)

# GPIO where traffic lights connected
RED_LIGHT_GPIO=22
YELLOW_LIGHT_GPIO=23
GREEN_LIGHT_GPIO=24

# Thermometer data GPIO
THERMOMETER_GPIO=4

LOG_FILE="temp.log"
IMAGE_FILE="temp.png"

ITER_DELAY_TIME=3
