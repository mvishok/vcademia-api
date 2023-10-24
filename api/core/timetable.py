import requests, json
from bs4 import BeautifulSoup
from .details import course
from module import constants

URL = 'https://academia.srmist.edu.in/srm_university/academia-academic-services/page/Unified_Time_Table_2023_Batch_1'

constants.HEADERS['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

def fetch(cookie):
    """
    The `fetch` function retrieves a timetable using a provided cookie and returns it in a dictionary
    format.
    
    :param cookie: The `cookie` parameter is a dictionary that contains various cookies required for
    making a request to a specific URL. The cookies are used to authenticate the request and provide
    necessary session information. The specific cookies used in this code are:
    :return: a dictionary with two keys: 'status' and 'timetable'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'timetable' is a dictionary
    containing timetable information.
    """
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'



    res = json.loads(requests.get(URL, headers=constants.HEADERS, cookies=cookie).text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')

    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[0]
    tr = table.findAll('tr')

    tt = {}

    for r in range(2, len(tr)):
        l = list(filter(None, tr[r].text.split('\n')))
        tt[l[0]] = l[1:]

    courses = course(cookie)['course']
    codes = {}
    for c in courses:
        codes[courses[c][6]] = courses[c][0]
    
    codes = {k2: v for k, v in codes.items() for k2 in (k.split('-') if '-' in k else [k])}

    for row in tt:
        for i in range(len(tt[row])):
            if tt[row][i] in codes:
                tt[row][i] = codes[tt[row][i]]
            else:
                tt[row][i] = '-'

    return {'status': 'success', 'timetable': tt}