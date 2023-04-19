from flask import Flask, redirect, url_for, render_template, request
import datetime

app = Flask(__name__)

scheduleTimes = [[0] * 2 for _ in range(4)] #column 0 is off column 1 is on, range 0 is lights, range 1 is filter, range 2 is pump, range 3 is temperature
tempPass = 0 #temperature being passed

@app.route("/")
def home():
   waterLevel = "12"
   waterTemperature = "100"
   airTemperature = "100"
   phLevel = "7"
   return render_template("home.html", waterLevel=waterLevel , waterTemperature=waterTemperature,
                          airTemperature=airTemperature, phLevel=phLevel)

@app.route("/devices")
def devices():
   return render_template("devices.html", scheduleTimes=scheduleTimes)

@app.route("/temperature")
def temperature():
   return render_template("temperature.html", scheduleTimes=scheduleTimes, tempPass=tempPass)

@app.route("/schedule")
def schedule():
   return render_template("schedule.html", scheduleTimes=scheduleTimes, tempPass=tempPass)

#@app.route("/login", methods=["POST","GET"])
#def login():
#    if request.method == "POST":
#        user = request.form["nm"]
#        return redirect(url_for("user", usr=user))
#    else:
#        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
