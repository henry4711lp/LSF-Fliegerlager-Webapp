from flask import Flask
from src.connection import dbconnector

# create flask app
app = Flask(__name__)


@app.route('/')
def connection():
    return dbconnector.sql("SELECT * FROM GETR")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
