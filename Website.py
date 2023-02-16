from flask import Flask

app = Flask(_main_)

def home():
    return "Hello this is the main page <hl>HELLO<hl>"

if _name_ == "main":
    app.run()
