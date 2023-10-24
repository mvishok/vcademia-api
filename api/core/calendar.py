import requests, json
from bs4 import BeautifulSoup
from module import constants

URL = "https://academia.srmist.edu.in/srm_university/academia-academic-services/page/Academic_Planner_2023_24_ODD"

constants.HEADERS['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

def fetch(cookie):
    """
    The `fetch` function fetches calendar data from Academia using a provided cookie and returns it in
    a structured format.
    
    :param cookie: The `cookie` parameter is a dictionary that contains various cookies used for making
    a request to a specific URL. The cookies are used to authenticate the request and provide additional
    information to the server. In this case, the `fetch` function uses the cookies to make a request to
    the specified URL and retrieve
    :return: a dictionary with two keys: 'status' and 'calendar'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'calendar' is a dictionary
    containing calendar data.
    """
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'

    res = json.loads(requests.get(URL, headers=constants.HEADERS, cookies=cookie).text)['HTML']
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