import json
from bs4 import BeautifulSoup
from .details import course

def fetch(session):
    res = json.loads(session.get('https://academia.srmist.edu.in/srm_university/academia-academic-services/page/Unified_Time_Table_2023_Batch_1').text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')

    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[0]
    tr = table.findAll('tr')

    tt = {}

    for r in range(2, len(tr)):
        l = list(filter(None, tr[r].text.split('\n')))
        tt[l[0]] = l[1:]

    courses = course(session)['course']
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