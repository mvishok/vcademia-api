import json
from bs4 import BeautifulSoup

def fetch(session):
    res = json.loads(session.get("https://academia.srmist.edu.in/srm_university/academia-academic-services/page/Academic_Planner_2023_24_ODD").text)['HTML']
    
    soup = BeautifulSoup(res, 'html.parser')
    table = BeautifulSoup(soup.find('div', class_='zc-pb-embed-placeholder-content').get('zmlvalue'), 'html.parser').findAll('table')[0]

    cal = {}

    ths = table.findAll('th')
    th = []
    for t in ths:
        if t.text != '':
            th.append(t.text[:7])

    th = [th[i: i+4] for i in range(0, len(th), 4)]
    for i in th:
        cal[i[2]] = [['Date', 'Day', 'Event', 'DO', '-']]
    th = [i for i in cal.keys()]

    trs = table.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        tds = [tds[i: i+5] for i in range(0, len(tds), 5)]
        for i in range(len(tds)):
            cal[th[i]].append([n.text for n in tds[i]])

    return {'status': 'success', 'calendar': cal}