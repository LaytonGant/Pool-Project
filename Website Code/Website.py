from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    # Initialize variables
    waterLevel = "12"
    waterTemperature = "100"
    airTemperature = "100"
    phLevel = "7"
    
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


if __name__ == "__main__":
    app.run(debug=True)
