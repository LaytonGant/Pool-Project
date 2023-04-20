'''
PoolManager.py
Author: Colin McBride
Date: April 19 2023
Version 1.1

A library for managing interactions with a pool controller 
with manual and automatic methods of control. 

========== VERSIONS ==========
v1.1 (4/19/23): Added control functionality with setStatus function.
v1.0 (4/7/23): Created file. Added basic request functionality. 
'''

from PoolCom import *
import sched, time

class PoolManager:
    # A custom exception used to report errors in use of Timer class
    class _TimerError(Exception):
        pass
    # --- end _TimerError

    # Timer class for any time-based functionality
    class _Timer:
        # --- Attributes ---
        # _start_time: The start time of the timer

        # Constructor
        def __init__(self):
            self._start_time = None

        # Start the timer
        def start(self):
            if self._start_time is None:
                self._start_time = time.perf_counter()
        
        # Stop the timer and return elapsed time in seconds
        def stop(self):
            if self._start_time is not None:
                elapsed_time = time.perf_counter() - self._start_time
                self._start_time = None
                return elapsed_time
            
        # Read the current value on the timer in seconds without stopping
        def read(self):
            if self._start_time is not None:
                return time.perf_counter() - self._start_time
            else:
                return 0
        
        # Read the hours component of the current time
        def readHour(self):
            totalTime = self.read()
            hours = totalTime // 3600   # floor division
            return hours
        
        def readMin(self):
            totalTime = self.read()
            mins = (totalTime - 3600*self.readHour()) % 60
            return mins
        
        # Read the seconds component of the current time
        def readSec(self):
            totalTime = self.read()
            secs = totalTime - 60*self.readMin() - 3600*self.readHour()
            return secs

    # --- end _Timer


    # --- Attributes ---
    # poolCom: PoolCom object for serial communication
    # devices: Dictionary mapping the device IDs to their name
    # file: File manager for reading/writing the schedule file. (not implemented)
    # schedManager: Scheduler object for maintaining time-based automation. (not implemented)

    PoolCom.initialize(9600,"COM7")

    isInit = False

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

    
    # PoolManager initializer. Initializes serial communication and 
    # file management. 
    def initialize():
        # Do not initialize more than once
        if PoolManager.isInit:
            return

        # Start pool com
        PoolManager.openCom()

        # Create scheduler
        # schedManager = sched.scheduler(time.time, time.sleep)

        PoolManager.isInit = True
    

    # Opens serial communication
    def openCom():
        # If com is not already open, open communication
        if not PoolCom.serialPort.is_open:
            PoolCom.start()


    # Closes serial communication
    def closeCom():
        # If com is not already closed, close communication
        if PoolCom.serialPort.is_open:
            PoolCom.stop()
    

    # Requests the status of every device on the pool controller. 
    # Returns a dictionary with each device name and status. 
    def reqFullStatus():
        # Initialize dictionary
        status = dict()

        # Request statuus of each device. Store in status dict. 
        for k in PoolManager.devices.keys():
            status[k] = PoolManager.reqStatus(k)

        # Return status
        return status


    # Requests the status of an individual device on the pool controller. 
    # Returns an integer representing the device status, or -1 if the device 
    # status could not be determined. 
    def reqStatus(device):
        # Do not request if COM port is not open
        if not PoolCom.serialPort.is_open:
            return -1

        # Port is open, try to request status
        if device in PoolManager.devices.keys():
            PoolCom.write(0, PoolManager.devices[device], 0)
            if PoolCom.goodRead:
                return PoolCom.data
            else:
                return -1
        else:
            return -1
        
    # Sets the status of an individual device on the pool controller. 
    # Returns an integer representing the device status, or -1 if the device
    # status could not be determined. 
    def setStatus(device, status):
        # Do not set if COM port is not open
        if not PoolCom.serialPort.is_open:
            return -1
        
        # Port is open, try to set status
        if device in PoolManager.devices.keys():
            PoolCom.write(1, PoolManager.devices[device], status)
            if PoolCom.goodRead:
                return PoolCom.data
            else:
                return -1
        else:
            return -1

      
    # Add a scheduled event


    # Remove a scheduled event


    # Read all scheduled events
    
