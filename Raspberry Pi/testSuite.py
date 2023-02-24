import RPi.GPIO as GPIO

# Setup
options = ["Output to pin", "Input from pin", "Change pin", "Quit"]
pin = 4
GPIO.setmode(GPIO.BCM)

# Output test
def output_test():
    GPIO.setup(pin,GPIO.OUT)
    sel = int(input("Enter 1 for high and 0 for low:"))
    GPIO.output(pin, (sel==1))

# Input test
def input_test():
    GPIO.setup(pin,GPIO.IN)
    print("Input on pin {}: {}".format(pin, GPIO.input(pin)))

# Pin select
def change_pin():
    sel = int(input("Enter new pin number: "))
    return sel

# Start test suite
print("IO Test Suite")
while True:
    print("----------")
    print("Selected pin:",pin)
    print("Enter an option:")
    for i in range(len(options)):
        print((i+1),options[i],sep='.')
    sel = int(input(">>"))
    if sel == 1:
        output_test()
    if sel == 2:
        input_test()
    if sel == 3:
        pin = change_pin()
    if sel == 4:
        break
GPIO.cleanup()

