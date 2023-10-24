from os import getenv
from cryptography.fernet import Fernet

key = getenv('CRYPTO_KEY')

def encrypt(data):
    """
    The function encrypts the given data using a key and returns the encrypted token.
    
    :param data: The `data` parameter is the data that you want to encrypt. It can be any type of data,
    such as a string, integer, or even a complex data structure like a dictionary or list
    :return: an encrypted token.
    """
    global key
    f = Fernet(key)
    token = f.encrypt(str(data).encode())
    return token

def decrypt(token):
    """
    The function `decrypt` takes a token as input, decrypts it using a global key, and returns the
    decrypted data.
    
    :param token: The `token` parameter is the encrypted data that needs to be decrypted
    :return: The decrypted data is being returned.
    """
    global key
    f = Fernet(key)
    data = f.decrypt(token).decode()
    return data
