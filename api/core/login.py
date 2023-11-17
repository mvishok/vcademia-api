import requests, json
from . import modules
from secrets import token_hex

def getSession(user, passw):
    header = {'Origin': 'https://academia.srmist.edu.in/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer': "'Referer': 'https://academia.srmist.edu.in/accounts/signin?_sh=false&hideidp=true&portal=10002227248&client_portal=true&dcc=true&servicename=ZohoCreator&service_language=en&serviceurl=https%3A%2F%2Facademia.srmist.edu.in%2F',"}
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
    with requests.Session() as session:
        req = session.post("https://academia.srmist.edu.in/accounts/signin.ac", data=payload, headers=header)
        res = json.loads(req.text)
        session.get(res['data']['oauthorize_uri'])
        if req.status_code == 200:
            if 'error' not in res.keys():
                return session
            else:
                return "ERROR:", res['error']
        else:
            return "ERROR:", req.status_code

def saveToken(user, passw):
    sess = getSession(user, passw)
    if not str(sess).startswith("ERROR"):
        key = token_hex(8)
        sql = """INSERT INTO sessions (key, un, pw) VALUES (%s, %s, %s)"""
        modules.cursor.execute(sql, (key, modules.encrypt(user).decode('utf-8'), modules.encrypt(passw).decode('utf-8')))
        return {'status': 'success', 'key': key}
    else:
        return sess[5:]
    
def fetchSession(key):
    sql = """SELECT un, pw FROM sessions WHERE key = %s"""
    modules.cursor.execute(sql, (key,))
    res = modules.cursor.fetchone()
    if res:
        return getSession(modules.decrypt(res[0]), modules.decrypt(res[1]))
    else:
        return {"status": "error", "error": "Invalid key"}