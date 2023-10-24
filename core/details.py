import requests, json
from bs4 import BeautifulSoup

from sys import path as syspath
from os import path as ospath
syspath.append(ospath.abspath(ospath.join(ospath.dirname(__file__), '..')))
from module import constants

URL = "https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Time_Table_2023_24"
URL2 = "https://academia.srmist.edu.in/srm_university/academia-academic-services/page/My_Attendance"

constants.HEADERS['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

def course(cookie):
    """
    The `course` function retrieves course information from Academia using cookies and returns it in a
    structured format.
    
    :param cookie: The `cookie` parameter is a dictionary that contains various cookies used for
    authentication and session management. These cookies are required to make a request to a specific
    URL and retrieve the course information
    :return: a dictionary with two keys: 'status' and 'course'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'course' is another dictionary
    containing information about courses.
    """
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'



    res = json.loads(requests.get(URL, headers=constants.HEADERS, cookies=cookie).text)['HTML']
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

def student(cookie):
    """
    The `student` function retrieves student details from Academia using cookies and returns them as a
    dictionary.
    
    :param cookie: The `cookie` parameter is a dictionary that contains various cookies used for making
    a request to a specific URL. The cookies are used to authenticate the request and provide session
    information. The specific cookies used in this code are:
    :return: a dictionary with two keys: 'status' and 'details'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'details' is another dictionary
    containing the details extracted from the HTML content.
    """
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'


    
    res = json.loads(requests.get(URL, headers=constants.HEADERS, cookies=cookie).text)['HTML']
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

def attendance(cookie):
    """
    The `attendance` function retrieves attendance data from Academia using cookies and returns it in a
    structured format.
    
    :param cookie: The `cookie` parameter is a dictionary that contains various cookies required for
    making a request to Academia. These cookies are used to authenticate the user and maintain their
    session. In the given code, the `attendance` function uses the `cookie` parameter to make a request
    to a specific URL and retrieve
    :return: a dictionary with two keys: 'status' and 'attendance'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'attendance' is another dictionary
    containing attendance information.
    """
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'



    res = json.loads(requests.get(URL2, headers=constants.HEADERS, cookies=cookie).text)['HTML']
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

        attendance[rows[indeces[i]+1].text.replace('Regular', '')] = l

    out = {'status': 'success', 'attendance': attendance}
    return out
    
def marks(cookie):
    """
    The function "marks" retrieves and parses course marks from Academia using a provided cookie.
    
    :param cookie: The `cookie` parameter is a dictionary that contains the necessary cookies for making
    the request. It is used to authenticate the user and access the required data
    :return: a dictionary with two keys: 'status' and 'marks'. The value of 'status' is 'success',
    indicating that the function executed successfully. The value of 'marks' is another dictionary
    containing the marks for each course. The keys of this inner dictionary are the course codes, and
    the values are lists containing the type of assessment (typ) and the mark for that assessment
    """

    codes = course(cookie)['course'].keys()
    
    
    cookie['ZCNEWUIPUBLICPORTAL']='true'



    res = json.loads(requests.get(URL2, headers=constants.HEADERS, cookies=cookie).text)['HTML']
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