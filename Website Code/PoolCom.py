'''
PoolCom.py
Author: Colin McBride
Date: April 7 2023
Version 1.1

A library for sending and receiving commands from an Arduino 
for a pool controller. 

========== VERSIONS ==========
v1.1 (4/7/23): Removed direct read functionality. Made write function also read the next input. 
v1.0 (3/30/23): Created file. Added basic init, read, and write functionality. 
'''

import serial

class PoolCom:
    # --- Attributes ---
    # serialPort:   Serial port object for communication. 
    # baud:         Baud rate of serial port. 
    # port:         Port to communicate over. 
    # goodRead:     Whether or not the last read attempt was successful. 
    # data:         Data of last successful read attempt. 

    # PoolCom constructor. Creates the serial port for communication.
    # baud: Baud rate for communication
    # port: COM port for communication. Set to the default for the Rasp. Pi. 
    def initialize(baud, port="/dev/ttyACM0"):
        PoolCom.baud = baud
        PoolCom.port = port
        PoolCom.goodRead = False
        PoolCom.data = "-1"
        PoolCom.serialPort = serial.Serial(baudrate=PoolCom.baud, timeout=3, write_timeout=1)
        PoolCom.serialPort.port = PoolCom.port
    
    # Starts communication on the PoolCom. 
    # Returns True if the port was successfully opened, False otherwise. 
    def start():
        try:
            PoolCom.serialPort.open()
            return True
        except:
            return False
        
    def stop():
        if (PoolCom.serialPort.is_open):
            PoolCom.serialPort.close()
    
    # Read function. Returns True if the read was successful, False otherwise. 
    # PoolCom.data is only updated if the read was successful. 
    # This is a private method, intended only to be used by the write() function
    # in the PoolCom class. 
    def _read():
        # Read message
        msg = PoolCom.serialPort.readline()

        # Check if any data was read
        if (len(msg) > 0):
            # Parse message
            msg = msg.decode("utf-8").strip()

            # Store data
            PoolCom.data = msg
            PoolCom.goodRead = True
            return True
        else:
            PoolCom.goodRead = False
            return False
    
    
    # Write function. Returns True if the write was successful, False otherwise. 
    # Also reads the next available input, storing the result of the read in 
    # the class attributes. 
    '''
    Communication Protocol: 
        Request Type
            0: Input/Status request
            1: Output/Control request
        Device
            Inputs
                00: Temp Sensor 1
                01: Temp Sensor 2
                02: pH Sensor
                03: Water Level Sensor
            Outputs
                10: Relay 1
                11: Relay 2
                12: Relay 3
                13: Relay 4
        Data
            Inputs
                0: Get status
            Outputs
                0: Turn device off
                1: Turn device on
    '''
    def write(reqType, device, data):
        msg = "{rt} {dv} {dt}".format(rt=reqType, dv=device, dt=data)
        try:
            PoolCom.serialPort.write(msg.encode("utf-8"))
            PoolCom._read()
            return True
        except:
            return False


