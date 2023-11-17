from os import getenv
from cryptography.fernet import Fernet
import psycopg2

key = getenv("CRYPTO_KEY")

connStr = getenv("DATABASE_URL")
conn = psycopg2.connect(connStr)
cursor = conn.cursor()
conn.autocommit = True

def encrypt(data):
    global key
    f = Fernet(key)
    token = f.encrypt(str(data).encode())
    return token

def decrypt(token):
    global key
    f = Fernet(key)
    data = f.decrypt(token).decode()
    return data