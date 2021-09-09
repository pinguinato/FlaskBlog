from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1 style='color:green;'>Hello World!</h1>"

@app.route("/contatti")
def contatti():
    return "Contattaci"