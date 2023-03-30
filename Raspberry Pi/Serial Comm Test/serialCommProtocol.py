from PoolCom import *
import time

# Make poolCom
poolCom = PoolCom(9600,"COM7")

# Try to start poolCom
comOpen = poolCom.start()

# Loop
while comOpen:
    # Input
    rt = input("Request Type: ")
    dv = input("Device: ")
    dt = input("Data: ")

    # Check to stop
    if (rt=="-1"):
        break

    # Write
    print("Sending info to Arduino...")
    if (poolCom.write(rt, dv, dt)):
        print("Success!")
    else:
        print("Error writing to Arduino.")

    # Read
    print("Reading info from Arduino...")
    if (poolCom.read()):
        print("Data received: " + poolCom.data)
    else:
        print("Error reading data from Arduino.")
    
    # Delay
    time.sleep(1)

# Stop
poolCom.stop()
