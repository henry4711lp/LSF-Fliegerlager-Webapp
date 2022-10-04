from flask import Flask, render_template, request
from src.connection import dbconnector

# create flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("start.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        vname = request.form["vname"]
        nname = request.form["nname"]

    return f"Hello {vname} {nname}!"


@app.route("/dbtest", methods=["POST", "GET"])
def dbtest():
        vname = "Test"
        nname = "User"
        sql_statement = f"SELECT ID FROM NAME WHERE VNAME = '{vname}' AND NNAME = '{nname}'"
        return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
