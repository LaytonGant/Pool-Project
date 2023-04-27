'''
PoolManager.py
Author: Colin McBride
Date: April 19 2023
Version 1.1

A library for managing interactions with a pool controller 
with manual and automatic methods of control. 

========== VERSIONS ==========
v1.2 (4/24/23): Added scheduling functionality
v1.1 (4/19/23): Added control functionality with setStatus function. Added filter timer. 
v1.0 (4/7/23): Created file. Added basic request functionality. 
'''

from PoolCom import *
import schedule, time, csv, threading


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
            return int(time.perf_counter() - self._start_time)
        else:
            return 0
    
    # Read the hours component of the current time
    def readHour(self):
        totalTime = self.read()
        hours = totalTime // 3600   # floor division
        return hours
    
    def readMin(self):
        totalTime = self.read()
        mins = (totalTime - 3600*self.readHour()) // 60
        return mins
    
    # Read the seconds component of the current time
    def readSec(self):
        totalTime = self.read()
        secs = totalTime - 60*self.readMin() - 3600*self.readHour()
        return secs
# --- end _Timer class


# A scheduled event struct to hold event data. 
# Every scheduled event acutally has 2 jobs: an on-job and an off-job. 
# * The on-job triggers when the device is scheduled to turn on
# * The off-job triggers when the devices is cheduled to turn off
class _SchedEvent:
    # --- Attributes ---
    # data (dict): Dictionary containing all data elements of the event
    #   id (int): Event ID
    #   device (str): Device the event controls
    #   onHour (int): Hour to turn device on
    #   onMin (int): Minute to turn device on
    #   offHour (int): Hour to turn device off
    #   offMin (int): Minute to turn device off
    # onJob (job): Job object associated with the on event in the scheduler
    # offJob (job): Job object associated with the off event in the scheduler

    # Constructor
    def __init__(self, id=-1, device=" ", onHour=-1, onMin=-1, offHour=-1, offMin=-1, data:dict=dict()):
        self.data = dict()
        if len(data) > 0:
            for (k,v) in data.items():
                # Make sure all integer values in the dict are cast as integers
                if not k=="device":
                    self.data[k] = int(v)
                else:
                    self.data[k] = v
        else:
            self.data = {
                "id": id,
                "device": device,
                "onHour": onHour,
                "onMin": onMin,
                "offHour": offHour,
                "offMin": offMin
            }
        self.onJob = None
        self.offJob = None
# --- end _SchedEvent


class PoolManager:
    # --- Attributes ---
    # PoolCom: Static PoolCom object for serial communication. 
    # devices: Dictionary mapping the device IDs to their name
    # pumpTimer: Timer to track how long the pump has been on. 
    # events: List of scheduled events
    # stopSchedEvent: Threading event that controls the scheduler thread. 
    #   Use "stopSchedEvent.set()" to stop the scheduler thread. 
    # targetTemp: Target temprature for when the heater is automatically controlled
    # stopHeaterEvent: Threading event that controls the automated heater thread. 
    #   Use "stopHeaterEvent.set()" t ostop the heater thread. 

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
    events:list[_SchedEvent] = list()
    _stopSchedEvent:threading.Event
    targetTemp = -1
    stopHeaterEvent:threading.Event = None

    
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
        
        # Read saved scheduled events
        with open('events.csv',newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                PoolManager.events.append(_SchedEvent(data=row))

        # Refresh events to add to scheduler
        PoolManager.refreshScheduler()

        # Start scheduler thread
        PoolManager._stopSchedEvent = PoolManager.runScheduler()

        # Pool manager initialized
        PoolManager.isInit = True
    

    def deinitialize():
        # Do not deinitialize more than once
        if not PoolManager.isInit:
            return

        # Stop pool com
        PoolManager.closeCom()

        # Save scheduled events to file
        PoolManager.saveEvents()

        # Stop scheduler thread
        PoolManager._stopSchedEvent.set()

        # Pool manager is deinitialized
        PoolManager.isInit = False
    

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
    

    # Creates a new event and adds it to the PoolManager.events list
    def createEvent(device, onHour, onMin, offHour, offMin):
        # Find next available id
        nextId = 0
        for e in PoolManager.events:
            if not e.data["id"] == nextId:
                break
            else:
                nextId += 1
        
        # Create new scheduled event
        newEvent = _SchedEvent(id=nextId, device=device, onHour=int(onHour), onMin=int(onMin), offHour=int(offHour), offMin=int(offMin))

        # Add to events list and scheduler
        PoolManager._addEvent(newEvent)
        PoolManager.events.append(newEvent)

        # Save new events to file
        PoolManager.saveEvents()
    

    # Deletes an existing event and removes it from the PoolManager.events list
    # If the id is not in the events list, nothing happens
    def deleteEvent(id):
        # Search for event with specified id
        for e in PoolManager.events:
            if e.data["id"] == id:
                PoolManager._removeEvent(e)
                PoolManager.events.remove(e)
        
        # Save results
        PoolManager.saveEvents()


    # Turns a given integer into a 2-digit string. Only works with positive integers. 
    def _doubleDigitize(num:int):
        if num < 10:
            return "0"+str(num)
        else:
            return str(num)


    # Adds an event to the scheduler
    def _addEvent(e: _SchedEvent):
        e.onJob = schedule.every().day.at("{}:{}".format(PoolManager._doubleDigitize(e.data["onHour"]), PoolManager._doubleDigitize(e.data["onMin"])))\
            .do(PoolManager.setStatus,e.data["device"],"1")
        e.offJob = schedule.every().day.at("{}:{}".format(PoolManager._doubleDigitize(e.data["offHour"]), PoolManager._doubleDigitize(e.data["offMin"])))\
            .do(PoolManager.setStatus,e.data["device"],"0")


    # Removes an event from the scheduler
    def _removeEvent(e: _SchedEvent):
        schedule.cancel_job(e.onJob)
        schedule.cancel_job(e.offJob)
        e.onJob = None
        e.offJob = None


    # Refreshes the events in the scheduler by clearing and re-adding all events. 
    # Also saves all events to a .csv file
    def refreshScheduler():
        schedule.clear()
        for e in PoolManager.events:
            PoolManager._addEvent(e)
        PoolManager.saveEvents()
    

    # Saves all current events to a file
    def saveEvents(fname="events.csv"):
        fileLabels = ["id", "device", "onHour", "onMin", "offHour", "offMin"]
        with open(fname, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fileLabels)
            writer.writeheader()
            for e in PoolManager.events:
                writer.writerow(e.data)


    # Function for continuously running the scheduler in a separate therad
    def runScheduler(interval=1):
        # Event to control thread execution
        stopEvent = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not stopEvent.is_set():
                    schedule.run_pending()
                    time.sleep(interval)
        
        # Create and start thread
        continuousThread = ScheduleThread()
        continuousThread.start()

        # Return stop event for external control
        return stopEvent
    

    # Function for continuously controlling the pool temperature in a separate thread
    def runHeaterControl(interval=60):
        # Stop any pre-existing threads
        if (not PoolManager.stopHeaterEvent==None) and (not PoolManager.stopHeaterEvent.is_set()):
            PoolManager.stopHeaterEvent.set()

        # Event to control thread execution
        stopEvent = threading.Event()

        class HeaterThread(threading.Thread):
            @classmethod
            def run(cls):
                while not stopEvent.is_set():
                    # Do temperature control stuff here
                    if not PoolManager.targetTemp==-1:
                        try:
                            # Get current temperature and heater status
                            currTemp = int(PoolManager.reqStatus("WaterTemp"))
                            heaterStatus = int(PoolManager.reqStatus("Heater"))
                            # Set heater based on current temperature
                            if (currTemp < PoolManager.targetTemp) and (heaterStatus==0):
                                PoolManager.setStatus("Heater",1)
                            elif (currTemp >= PoolManager.targetTemp) and (heaterStatus==1):
                                PoolManager.setStatus("Heater",0)
                        except:
                            pass

                        # Sleep
                        time.sleep(interval)
        
        # Create and start thread
        continuousThread = HeaterThread()
        continuousThread.start()

        # Return stop event for external control
        return stopEvent

# --- end PoolManager class
