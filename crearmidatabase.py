# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector
import os

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = os.getenv('DB_PASSWORD')
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE ferreteria")

print("Listo!")