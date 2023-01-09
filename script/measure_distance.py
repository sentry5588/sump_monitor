# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# TODO: Make code robust (e.g. take average)
# TODO: Use error code 

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
MEASUREMENT_INTERVAL_SEC = 1

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance() -> tuple:
    '''
    Return (flag, value)
    Flag = 0, error, value = error code
    Flag = 1, normal, value = distance in cm
    '''
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    counter = 0 # User counter to exit from deadloop due to hardware
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        counter += 1
        if counter == 5000:
            return (0, 1)

    # save time of arrival
    counter = 0 # User counter to exit from deadloop due to hardware
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        counter += 1
        if counter == 50000:
            return (0, 2)

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return (1, distance)

if __name__ == '__main__':
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
    time.sleep(2)  # wait for the sensor to settle
    print("Sump basin level measuring started")

    try:
        while True:
            flag, dist = distance()
            print("Water is {0:.0f} cm to the basement floor".format(dist))
            time.sleep(MEASUREMENT_INTERVAL_SEC)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
