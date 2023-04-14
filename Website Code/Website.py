from flask import Flask, redirect, url_for, render_template, request
from PoolManager import *

# Initialization
app = Flask(__name__)

# Home page
@app.route("/", methods=["GET","POST"])
def home():
    # Initialize pool manager
    if not PoolManager.isInit:
        PoolManager.initialize()

    # Request status of pool controller
    status = PoolManager.reqFullStatus()

    # Initialize variables
    waterLevel = status["WaterLevel"]
    waterTemperature = status["WaterTemp"]
    airTemperature = status["AirTemp"]
    phLevel = status["pH"]
    pump = status["Pump"] == 1
    heater = status["Heater"] == 1
    filter = status["Filter"] == 1
    lights = status["Lights"] == 1
    
    # Check request type
    # POST
    if request.method == "POST":
       app.logger.info("Post request")
       postFunc("pumpSwitch")
       postFunc("lightsSwitch")
       postFunc("filterSwitch")
    
    # GET
    else:
        app.logger.info("Get request")
    
    # Render template
    return render_template("Website.html", waterLevel=waterLevel , waterTemperature=waterTemperature,
                        airTemperature=airTemperature, phLevel=phLevel, pump=pump, heater=heater, 
                        filter=filter, lights=lights)


def postFunc(elem):
    if elem in request.form:
        formVal = request.form[elem]
        app.logger.info("Checkbox value:"+formVal)

# Debug
if __name__ == "__main__":
    app.run(debug=True)

