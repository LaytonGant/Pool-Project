from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
       app.logger.info("Post request")
       chckbxVal = request.form["chkbx1"]
       app.logger.info("Checkbox value:"+chckbxVal)
    else:
        app.logger.info("Get request")
    waterLevel = "12"
    waterTemperature = "100"
    airTemperature = "100"
    phLevel = "7"
    return render_template("Website.html", waterLevel=waterLevel , waterTemperature=waterTemperature,
                          airTemperature=airTemperature, phLevel=phLevel)

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
