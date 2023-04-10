'''
PoolManager.py
Author: Colin McBride
Date: April 7 2023
Version 1.1

A library for managing interactions with a pool controller 
with manual and automatic methods of control. 

========== VERSIONS ==========
v1.1 (4/10/23): Added scheduling functionality. 
v1.0 (4/7/23): Created file. Added basic request functionality. 
'''

import PoolCom
import sched, time

class PoolManager:
    # --- Attributes ---
    # poolCom: PoolCom object for serial communication
    # file: File manager for reading/writing the schedule file. 
    # devices: Dictionary mapping the device IDs to their name
    # schedManager: Scheduler object for maintaining time-based automation. 

    devices = {
        # Input devices
        "AirTemp"    : 0,
        "WaterTemp"  : 1,
        "pH"         : 2,
        "WaterLevel" : 3,
        # Output devices
        "Pump"   : 10,
        "Filter" : 11,
        "Heater" : 12,
        "Lights" : 13
    }


    # PoolManager constructor. Initializes serial communication and 
    # file management. 
    def __init__(self):
        # Make and start pool com
        self.poolCom = PoolCom(9600,"COM8")
        self.poolCom.start()
        schedManager = sched.scheduler(time.time, time.sleep)
    

    # Opens serial communication
    def openCom(self):
        # If com is not already open, open communication
        if not self.poolCom.serialPort.is_open:
            self.poolCom.start()


    # Closes serial communication
    def closeCom(self):
        # If com is not already closed, close communication
        if self.poolCom.serialPort.is_open:
            self.poolCom.stop()
    

    # Requests the status of every device on the pool controller. 
    # Returns a dictionary with each device name and status. 
    def reqFullStatus(self):
        # Initialize dictionary
        status = dict()

        # Request statuus of each device. Store in status dict. 
        for k in self.devices.keys():
            status[k] = self.reqStatus(k)

        # Return status
        return status


    # Requests the status of an individual device on the pool controller. 
    # Returns an integer representing the device status, or -1 if the device 
    # status could not be determined. 
    def reqStatus(self, device):
        if device in self.devices.keys():
            self.poolCom.write(0,self.devices[device],0)
            if self.poolCom.goodRead:
                return self.poolCom.data
            else:
                return -1
        else:
            return -1

      
    # Add a scheduled event


    # Remove a scheduled event


    # Read all scheduled events
    
