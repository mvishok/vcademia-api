import json
from bs4 import BeautifulSoup
      
def course(session):
    res = json.loads(session.get("https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Time_Table_2023_24").text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[1]
    rows = table.findAll('td')
    size = len(rows)
    indeces = [i for i in range(0,size+1,12)]

    course = {}
    for i in range(0,len(indeces)-1):
        l = [
            rows[indeces[i]+2].text,
            rows[indeces[i]+3].text,
            rows[indeces[i]+4].text,
            rows[indeces[i]+5].text,
            rows[indeces[i]+6].text,
            rows[indeces[i]+7].text,
            rows[indeces[i]+8].text,
            rows[indeces[i]+9].text,
            rows[indeces[i]+10].text,
            rows[indeces[i]+11].text
        ]
        course[rows[indeces[i]+1].text] = l

    return {'status': 'success', 'course': course}

def student(session):
    res = json.loads(session.get("https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Time_Table_2023_24").text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[0]
    rows = table.findAll('td')
    
    # make a dict with rows[i]:rows[i+1]
    details = {}
    for i in range(0,len(rows),2):
        details[rows[i].text] = rows[i+1].text

    return {'status': 'success', 'details': details}

def attendance(session):
    res = json.loads(session.get("https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Attendance").text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[2]
    rows = table.findAll('td')

    indeces = [i for i in range(0, len(rows), 8)]

    attendance = {}
    for i in range (0, len(indeces)):
        l = [
            rows[indeces[i]+2].text,
            rows[indeces[i]+3].text,
            rows[indeces[i]+4].text,
            rows[indeces[i]+5].text,
            rows[indeces[i]+6].text,
            rows[indeces[i]+7].text
        ]

        attendance[rows[indeces[i]+1].text.replace('Regular', '')+" "+rows[indeces[i]+3].text] = l

    out = {'status': 'success', 'attendance': attendance}
    return out

def marks(session):
    codes = course(session)['course'].keys()

    res = json.loads(session.get("https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Attendance").text)['HTML']
    res = res[res.find("sanitize(")+9:res.find("');function doaction")].replace("\\\\","\\").encode().decode('unicode-escape')
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.findAll('table')[3]
    rows = table.findAll('td')
    marks={}

    for i in range(3, len(rows)):
        if rows[i].text in codes:
            code = rows[i].text
            typ = rows[i+1].text

            if 'Abs' in str(rows[i+2]):
                mark = 'AB'
            elif rows[i+2].text == '':
                mark = 'NA'
            else:
                mark = str(rows[i+2]).split('<br/>')[-1].split('</font')[0] +"/"+ str(rows[i+2]).split('<strong>')[-1].split('</strong>')[0].split('/')[-1] 
            marks[code] = [typ, mark]
    out = {'status': 'success', 'marks': marks}
    return out