from flask import Flask, redirect, url_for, render_template, request
from PoolManager import *

app = Flask(__name__)

scheduleTimes = [[0] * 2 for _ in range(4)] #column 0 is off column 1 is on, range 0 is lights, range 1 is filter, range 2 is pump, range 3 is temperature
tempPass = 0 #temperature being passed

def startPoolManager():
   if not PoolManager.isInit:
      PoolManager.initialize()

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
   # Initialize Pool Manager
   startPoolManager()

   # Get full status
   status = PoolManager.reqFullStatus()

   # Set values
   waterLevel = "High" if int(status["WaterLevel"])==0 else "Low"
   waterTemperature = status["WaterTemp"]
   airTemperature = status["AirTemp"]
   phLevel = status["pH"]
   heaterStatus = "On" if int(status["Heater"])==1 else "Off"
   filterStatus = "On" if int(status["Filter"])==1 else "Off"
   if int(status["Pump"])==1:
      pumpStatus = [PoolManager.pumpTimer.readHour(), PoolManager.pumpTimer.readMin(), PoolManager.pumpTimer.readSec()]
   else:
      pumpStatus = [0, 0, 0]

   return render_template("home.html", waterLevel=waterLevel , waterTemperature=waterTemperature,
                          airTemperature=airTemperature, phLevel=phLevel, heaterStatus=heaterStatus, 
                          filterStatus=filterStatus,  pumpStatus=pumpStatus)

# Devices page
@app.route("/devices", methods=["GET", "POST"])
def devices():
   # Initialize pool manager
   startPoolManager()

   # GET
   if request.method == "GET":
      # Fetch device states
      status = PoolManager.reqFullStatus()
   
      # Set values
      pumpState = status["Pump"]
      filterState = status["Filter"]
      heaterState = status["Heater"]
      lightState = status["Lights"]

      # Render webpage
      return render_template("devices.html", pumpState=pumpState, filterState=filterState, heaterState=heaterState, 
                              lightState=lightState, scheduleTimes=scheduleTimes)
   # --- end if GET

   # POST
   else:
      # Determine if this is control form or schedule form
      if not "starttm" in request.form:
         # Determine status
         if "status" in request.form.keys():
            isOn = 1
         else:
            isOn = 0
         # Perform device control
         PoolManager.setStatus(request.form["device"], isOn)
      else:
         # Parse start and end times
         (onHour, onMin) = request.form["starttm"].split(":")
         (offHour, offMin) = request.form["endtm"].split(":")

         # Add new control event
         PoolManager.createEvent(device=request.form["schedDevice"], onHour=onHour, onMin=onMin, offHour=offHour, offMin=offMin)

      # Return 
      return render_template("devices.html")
   # --- end if POST
# --- end devices()

   

# Temperature page
@app.route("/temperature", methods=["GET", "POST"])
def temperature():
   # Initialize pool manager
   startPoolManager()

   # Temperature change request
   if request.method == "POST":
      # Determine if this is a control or schedule form
      if not "starttm" in request.form:
         # Set target temperature
         PoolManager.targetTemp = int(request.form["temperatureValue"])

         # If checkbox is selected, enable auto heater control
         if "enableTemp" in request.form:
            PoolManager.stopHeaterEvent = PoolManager.runHeaterControl()
         else:
            if not PoolManager.stopHeaterEvent==None:
               PoolManager.stopHeaterEvent.set()
      else:
         # Parse start and end times
         (onHour, onMin) = request.form["starttm"].split(":")
         (offHour, offMin) = request.form["endtm"].split(":")

         # Add new control event
         PoolManager.createEvent(device="Heater", onHour=onHour, onMin=onMin, offHour=offHour, offMin=offMin)

   # Check if target temp is set
   if not PoolManager.targetTemp==-1:
      waterTemperature = PoolManager.targetTemp
   # If not, retrieve water temperature
   else:
      waterTemperature = PoolManager.reqStatus("WaterTemp")
   
   # Check if auto-heater is on
   if (not PoolManager.stopHeaterEvent==None) and (not PoolManager.stopHeaterEvent.is_set()):
      autoHeater = True
   else:
      autoHeater = False

   # Render webpage
   return render_template("temperature.html", waterTemperature=waterTemperature, autoHeater=autoHeater, scheduleTimes=scheduleTimes, tempPass=tempPass)


# Schedule page
@app.route("/schedule")
def schedule():
   # Initialize pool manager
   startPoolManager()

   # Read scheduled events from PoolManager
   events = PoolManager.events

   # Render webpage
   return render_template("schedule.html", events=events, tempPass=tempPass)

# Trying to call data from the temp page and the devices page
@app.route('/timing', methods=['POST', 'GET'])
def timing():
   print("Timing Function")
   if 'starttm' in request.form:
      start_time=request.form['starttm']
      print("Start Time: {}".format(start_time))
   elif 'endtm' in request.form:
      end_time=request.form['endtm']
      print("End Time: {}".format(end_time))
   else:
      return "Missing St or Et"
   
#@app.route("/login", methods=["POST","GET"])
#def login():
#    if request.method == "POST":
#        user = request.form["nm"]
#        return redirect(url_for("user", usr=user))
#    else:
#        return render_template("login.html")

if __name__ == "__main__":
   # Run as private server
   app.run(debug=True)
   # Run as public server
   # app.run(debug=True, host='0.0.0.0', port='5000')

   # Deinitialize PoolManager
   PoolManager.deinitialize()
