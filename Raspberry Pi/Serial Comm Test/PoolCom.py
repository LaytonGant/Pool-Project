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
    def __init__(self, baud, port="/dev/ttyACM0"):
        self.baud = baud
        self.port = port
        self.goodRead = False
        self.data = "-1"
    
    # Starts communication on the PoolCom. 
    # Returns True if the port was successfully opened, False otherwise. 
    def start(self):
        try:
            self.serialPort = serial.Serial(self.port, self.baud, timeout=5, write_timeout=1)
            return True
        except:
            return False
        
    def stop(self):
        if (self.serialPort.is_open):
            self.serialPort.close()
    
    # Read function. Returns True if the read was successful, False otherwise. 
    # self.data is only updated if the read was successful. 
    def read(self):
        # Read message
        msg = self.serialPort.readline()

        # Check if any data was read
        if (len(msg) > 0):
            # Parse message
            msg = msg.decode("utf-8").strip()

            # Store data
            self.data = msg
            self.goodRead = True
            return True
        else:
            self.goodRead = False
            return False
    
    # Write function. Returns True if the write was successful, False otherwise. 
    def write(self, reqType, device, data):
        msg = "{rt} {dv} {dt}".format(rt=reqType, dv=device, dt=data)
        try:
            self.serialPort.write(msg.encode("utf-8"))
            return True
        except:
            return False


