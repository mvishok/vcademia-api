from os import getenv
from cryptography.fernet import Fernet

key = getenv("CRYPTO_KEY")

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