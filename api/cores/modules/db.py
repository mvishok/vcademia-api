import psycopg2
from os import getenv

connStr = getenv('DATABASE_URL')
conn = psycopg2.connect(connStr)
cursor = conn.cursor()
conn.autocommit = True

