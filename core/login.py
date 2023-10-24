import requests
import json
from secrets import token_hex

from sys import path as syspath
from os import path as ospath
syspath.append(ospath.abspath(ospath.join(ospath.dirname(__file__), '..')))
from module import crypto, db, constants

URL = "https://academia.srmist.edu.in/accounts/signin.ac"


def getCookies(user, passw):
    """
    The getCookies function sends a POST request with user credentials to a specified URL, retrieves
    cookies from the response, and returns them as a token.
    
    :param user: The `user` parameter is the username or email address of the user trying to log in
    :param passw: The `passw` parameter is the password for the user's account
    :return: a dictionary with the following keys:
    - "status": indicating the status of the request ("success" or "error")
    - "token": containing the cookies obtained from the request, if the request was successful
    - "error": containing the error message, if there was an error in the request
    """
    payload = {
        'username': user,
        'password': passw,
        'client_portal': 'true',
        'portal': '10002227248',
        'servicename': 'ZohoCreator',
        'serviceurl': 'https://academia.srmist.edu.in/',
        'grant_type': 'password',
        'service_language': 'en',
        'is_ajax': 'true',
        'dcc': 'true'
    }

    try:
        res = requests.post(URL, data=payload, headers=constants.HEADERS)
        res = json.loads(res.text)
        
        if 'error' in res.keys():
            return {"status": "error", "error": res['error']}
        
        session = requests.Session()
        session.get(res['data']['oauthorize_uri'], headers=constants.HEADERS)
        cookies = session.cookies.get_dict()
        res = {"status": "success", "token": cookies}

    except Exception as e:
        res = {"status": "error", "error": str(e)}

    return res

def saveCookies(cookies):
    """
    The function saves encrypted cookies in a database table and returns a unique key for the saved
    cookies.
    
    :param cookies: The "cookies" parameter is a string that represents the cookies data that needs to
    be saved
    :return: either the generated key or the string "DBERROR" depending on the outcome of the try block.
    """
    try:
        key = token_hex(8)
        cookies = crypto.encrypt(cookies).decode('utf-8')
        sql = """INSERT INTO sessions (`key`, `session`) VALUES (%s, %s)"""
        db.cursor.execute(sql, (key, cookies))
        return key
    except Exception as e:
        return "DBERROR"

def fetchCookies(key):
    """
    The function fetchCookies retrieves a session cookie from a database using a given key, decrypts it,
    and returns it along with a success status, or returns an error status if the key is invalid.
    
    :param key: The `key` parameter is a unique identifier used to retrieve a session cookie from the
    database
    :return: The function fetchCookies returns a dictionary with two keys: "status" and either "cookie"
    or "error". If the key is valid and a session is found in the database, the status is set to
    "success" and the decrypted session cookie is returned as the value for the "cookie" key. If the key
    is invalid or no session is found, the status is set to "error
    """
    sql = """SELECT session FROM sessions WHERE `key` = %s"""
    db.cursor.execute(sql, (key,))
    res = db.cursor.fetchone()
    if res:
        return {"status": "success", "cookie": crypto.decrypt(res[0].encode('utf-8'))}
    else:
        return {"status": "error", "error": "Invalid key"}

def getKey(user, passw):
    """
    The function `getKey` takes a username and password as input, retrieves cookies using the
    `getCookies` function, and returns a dictionary containing the status and key if successful, or an
    error message if unsuccessful.
    
    :param user: The "user" parameter is the username or user ID of the user trying to log in
    :param passw: The parameter "passw" is likely the password for the user
    :return: a dictionary with two keys: "status" and either "key" or "error". If the status is
    "success", it will also include the key value.
    """
    cookies = getCookies(user, passw)
    if cookies['status'] == 'success':
        key = saveCookies(str(cookies['token']))
        return {"status": "success", "key": key}
    else:
        return {"status": "error", "error": cookies['error']}