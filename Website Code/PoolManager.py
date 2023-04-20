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


# A custom exception used to report errors in use of Timer class
class _TimerError(Exception):
    pass
# --- end _TimerError class

# Timer class for any time-based functionality
class _Timer:
    # --- Attributes ---
    # _start_time: The start time of the timer
    # isRunning: Whether the timer is running or not 

    # Constructor
    def __init__(self):
        self._start_time = None
        self.isRunning = False

    # Start the timer
    def start(self):
        if self._start_time is None:
            self._start_time = time.perf_counter()
            self.isRunning = True
    
    # Stop the timer and return elapsed time in seconds
    def stop(self):
        if self._start_time is not None:
            elapsed_time = time.perf_counter() - self._start_time
            self._start_time = None
            self.isRunning = False
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

# --- end _Timer class


class PoolManager:
    # --- Attributes ---
    # poolCom: PoolCom object for serial communication
    # devices: Dictionary mapping the device IDs to their name
    # pumpTimer: Timer to track how long the pump has been on. 
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

    pumpTimer = _Timer()

    
    # PoolManager initializer. Initializes serial communication and 
    # file management. 
    def initialize():
        # Do not initialize more than once
        if PoolManager.isInit:
            return

        # Start pool com
        PoolManager.openCom()

        # If com is open, send an initial communication
        if PoolCom.serialPort.is_open:
            PoolCom.write(0,0,0)

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
            # Request status
            PoolCom.write(0, PoolManager.devices[device], 0)

            # Check if good read
            if PoolCom.goodRead:
                # If pump is on, check pump timer
                if device=="Pump": 
                    # If pump is on and timer is not, start timer
                    if int(PoolCom.data)==1 and not PoolManager.pumpTimer.isRunning:
                        PoolManager.pumpTimer.start()
                    # If pump is off and timer is on, stop timer
                    if int(PoolCom.data)==0   and PoolManager.pumpTimer.isRunning:
                        PoolManager.pumpTimer.stop()

                # Return device status
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
        
        # If device if pump, start/stop timer
        if device=="Pump":
            if int(status)==1 and not PoolManager.pumpTimer.isRunning:
                PoolManager.pumpTimer.start()
            if int(status)==0 and PoolManager.pumpTimer.isRunning:
                PoolManager.pumpTimer.stop()
        
        # Port is open, try to set status
        if device in PoolManager.devices.keys():
            PoolCom.write(1, PoolManager.devices[device], status)
            if PoolCom.goodRead:
                return PoolCom.data
            else:
                return -1
        else:
            return -1

    
# --- end PoolManager class
