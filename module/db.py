import mysql.connector
from os import getenv

db = mysql.connector.connect(
    host=getenv('DB_HOST'),
    user=getenv('DB_USER'),
    passwd=getenv('DB_PASS'),
    database="academia"
)

cursor = db.cursor()

