import webiopi
import datetime

GPIO = webiopi.GPIO

LIGHT = 4 # GPIO pin using BCM numbering

# setup function called at WebIOPi startup
def setup():
    # set GPIO used
    GPIO.setFunction(LIGHT, GPIO.OUT)


# loop function is repeadedly called by WebIOPi
def loop():
    # toggle light
    if (GPIO.digitalRead(LIGHT) == GPIO.LOW):
        GPIO.digitalWrite(LIGHT, GPIO.HIGH)
    else:
        GPIO.digitalWrite(LIGHT, GPIO.LOW)

    # delay between loops
    webiopi.sleep(500)

# destroy function called on WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(LIGHT, GPIO.LOW)
