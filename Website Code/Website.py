from flask import Flask, redirect, url_for, render_template, request
from PoolManager import *

# Initialization
app = Flask(__name__)
poolManager = PoolManager()

# Home page
@app.route("/", methods=["GET","POST"])
def home():
    # Initialize pool manager
    poolManager.openCom()

    # Requuest status of pool controller
    status = poolManager.reqFullStatus()

    # Initialize variables
    waterLevel = status["WaterLevel"]
    waterTemperature = status["WaterTemp"]
    airTemperature = status["AirTemp"]
    phLevel = status["pH"]
    
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
                        airTemperature=airTemperature, phLevel=phLevel)


def postFunc(elem):
    if elem in request.form:
        formVal = request.form[elem]
        app.logger.info("Checkbox value:"+formVal)


# Debug
if __name__ == "__main__":
    app.run(debug=True)
