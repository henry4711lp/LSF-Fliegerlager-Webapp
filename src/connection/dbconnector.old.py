from _mysql_connector import MySQL
from flask import app

app.config['MYSQL_HOST'] = '10.0.0.104'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Keksdose123'
app.config['MYSQL_DB'] = 'Strichliste'

mysql = MySQL(app)




def exec_sql(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()
    return cursor.fetchone()



@app.route('/')
def index():
    data = exec_sql("SELECT * FROM GETR")
    print(data)
    print("alive")
    return "test"