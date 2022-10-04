from flask import Flask, render_template, request
from src.connection import dbconnector

# create flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("start.html")


@app.route('/register')
def index():
    return render_template("register.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    name = ""
    if request.method == "POST":
        name = request.form["vname"]

    return f"Hello {name}!"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
