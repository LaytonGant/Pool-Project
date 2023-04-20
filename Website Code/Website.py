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

   # POST
   else:
      # For a post request, use the last full status values
      #status = lastFullStatus

      # Determine status
      if "status" in request.form.keys():
         isOn = 1
      else:
         isOn = 0

      # Perform device control
      PoolManager.setStatus(request.form["device"], isOn)

      # Return 
      return render_template("devices.html")

   

# Temperature page
@app.route("/temperature", methods=["GET", "POST"])
def temperature():
   # Initialize pool manager
   startPoolManager()

   # Retrieve water temperature
   waterTemperature = PoolManager.reqStatus("WaterTemp")

   # Temperature change request
   if request.method == "POST":
      # If temperature is higher, turn on heater
      if int(request.form["temperatureValue"]) > waterTemperature:
         PoolManager.setStatus("Heater",1)
      else:
         PoolManager.setStatus("Heater",0)

   # Render webpage
   return render_template("temperature.html", waterTemperature=waterTemperature, scheduleTimes=scheduleTimes, tempPass=tempPass)

# Schedule page
@app.route("/schedule")
def schedule():
   # Initialize pool manager
   startPoolManager()

   # Render webpage
   return render_template("schedule.html", scheduleTimes=scheduleTimes, tempPass=tempPass)

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
