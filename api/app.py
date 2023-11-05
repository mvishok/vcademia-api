from flask import Flask, jsonify, request
from flasgger import Swagger
from api.cores import login, details, timetable, calendar
import json

app = Flask(__name__)
app.config['url_sort_key'] = None
app.config['SWAGGER'] = {
    'title': 'Vcademia API',
    'uiversion': 3,
    'hide_top_bar': True,
    'specs_route': '/',
    'css': '/static/css/theme-newspaper.css',
    "ui_params": {
        "tagsSorter": "alpha"
    }
}

#swagger template to define authkey headers
SWAGGER_TEMPLATE = {"securityDefinitions": {"AccessKey": {"type": "apiKey", "name": "x-access-token", "in": "header"}}}

swagger = Swagger(app, template=SWAGGER_TEMPLATE)

@app.route('/ping', methods=['GET'])
def ping():
    """
    Endpoint to check server status
    ---
    tags:
        - Status
    summary: Check server status
    description: This endpoint checks the status of the server.
    responses:
        200:
            description: Server is running
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: success
                    message:
                        type: string
                        example: Server is running
    """
    return jsonify({'status': 'success', 'message': 'Server is running'})

@app.route('/key', methods=['POST'])
def get_access():
    """
    Endpoint to get access key
    ---
    tags:
        - Authentication
    summary: Get access key for a user
    description: This endpoint retrieves an access key for a user.
    consumes:
        - application/x-www-form-urlencoded
    parameters:
        - name: user
          in: formData
          type: string
          required: true
          description: Username (Net ID including @srmist.edu.in)
        - name: pass
          in: formData
          type: string
          required: true
          description: Password

    responses:
        200:
            description: Access key retrieved successfully
            schema:
                type: object
                properties:
                    access_key:
                        type: string
        401:
            description: Unauthorized
    """
    try:
        username = request.form['user']
        password = request.form['pass']
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    res = login.getKey(username, password)
    return jsonify(res)

@app.route('/course', methods=['GET'])
def get_course():
    """
    Endpoint to get course details
    ---
    tags:
        - Portal Information
    summary: Get course details using an access key
    description: This endpoint retrieves course details based on the provided access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Course details retrieved successfully
            schema:
                type: object
                properties:
                    course:
                        type: object
                        properties:
                            "Course Code":
                                type: array
                                items:
                                    type: array
                            "status":
                                type: string
                        example:
                            "Course Code": [
                                "Course Title",
                                "Credit",
                                "Registration Type",
                                "Category",
                                "Course Type",
                                "Faculty Name",
                                "Slot",
                                "GCR Code",
                                "Room Number",
                                "Academic Year"
                            ]
                            "status": "success"
    """
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))
    
    try:
        res = details.course(cookie)
    except:
        return jsonify({'status': 'error', 'message': 'Error processing request, please try again later'})
    return jsonify(res)

@app.route('/details', methods=['GET'])
def get_details():
    """
    Endpoint to get student details
    ---
    tags:
        - Portal Information
    summary: Get student details using an access key
    description: This endpoint retrieves student details for a user using an access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Student details retrieved successfully
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: success
                    details:
                        type: object
                        properties:
                            "Class Room:":
                                type: integer
                                example: "000"
                            "Combo / Batch:":
                                type: string
                                example: "0/0"
                            Department:
                                type: string
                                example: "Department Name (A1 - Section)"
                            Mobile:
                                type: integer
                                example: "0000000000"
                            Name:
                                type: string
                                example: "Student Name"
                            Program:
                                type: string
                                example: "Enrolled Programme"
                            "Registration Number:":
                                type: string
                                example: "RA0000000000000"
                            Semester:
                                type: integer
                                example: "0"
        401:
            description: Unauthorized
        500:
            description: Internal Server Error
    """
    
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))
    
    try:
        res = details.student(cookie)
    except:
        return jsonify({'status': 'error', 'message': 'Error processing request, please try again later'})
    
    return jsonify(res)

@app.route('/attendance', methods=['GET'])
def get_attendance():
    """
    Endpoint to get attendance details
    ---
    tags:
        - Portal Information
    summary: Get attendance details using an access key
    description: This endpoint retrieves attendance details for a user using an access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Attendance details retrieved successfully
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: success
                    attendance:
                        type: object
                        properties:
                            Course Title:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        Category:
                                            type: string
                                            example: "Category"
                                        "Faculty Name":
                                            type: string
                                            example: "Faculty Name"
                                        Slot:
                                            type: string
                                            example: "Slot"
                                        "Hours Conducted":
                                            type: string
                                            example: "Hours Conducted"
                                        "Hours Absent":
                                            type: string
                                            example: "Hours Absent"
                                        Attendance:
                                            type: string
                                            example: "Attendance"
        401:
            description: Unauthorized
        500:
            description: Internal Server Error
    """
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))
    
    try:
        res = details.attendance(cookie)
    except:
        return jsonify({'status': 'error', 'message': 'Error processing request, please try again later'})
    
    return jsonify(res)

@app.route('/marks', methods=['GET'])
def get_marks():
    """
    Endpoint to get marks details
    ---
    tags:
        - Portal Information
    summary: Get marks details using an access key
    description: This endpoint retrieves marks details for a user using an access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Marks details retrieved successfully
            schema:
                type: object
                properties:
                    status:
                        type: string
                        example: success
                    marks:
                        type: object
                        properties:
                            Course Code:
                                type: array
                                items:
                                    type: string
                                    example: "Course Type"
                            "Test Performance":
                                type: array
                                items:
                                    type: string
                                    example: "Test Performance"
        401:
            description: Unauthorized
        500:
            description: Internal Server Error
    """
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))
    
    try:
        res = details.marks(cookie)
    except:
        return jsonify({'status': 'error', 'message': 'Error processing request, please try again later'})
    return jsonify(res)

@app.route('/timetable', methods=['GET'])
def get_timetable():
    """
    Endpoint to get timetable details
    ---
    tags:
        - Portal Information
    summary: Get timetable details using an access key
    description: This endpoint retrieves timetable details based on the provided access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Timetable details retrieved successfully
            schema:
                type: object
                properties:
                    timetable:
                        type: object
                        properties:
                            "Hour/Day Order":
                                type: array
                                items:
                                    type: string
                            status:
                                type: string
                        example:
                            "Hour/Day Order": [
                                "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"
                            ]
                            "status": "success"
    """
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))
    
    try:
        res = timetable.fetch(cookie)
    except:
        return jsonify({'status': 'error', 'message': 'Error processing request, please try again later'})
    
    return jsonify(res)

@app.route('/calendar', methods=['GET'])
def get_calendar():
    """
    Endpoint to get calendar details
    ---
    tags:
        - Portal Information
    summary: Get calendar details using an access key
    description: This endpoint retrieves calendar details based on the provided access key.
    consumes:
        - application/x-www-form-urlencoded
    security:
        - AccessKey: ['x-access-token']

    responses:
        200:
            description: Calendar details retrieved successfully
            schema:
                type: object
                properties:
                    calendar:
                        type: object
                        properties:
                            "MMM 'YY":
                                type: array
                                items:
                                    type: array
                                    items:
                                        type: string
                            status:
                                type: string
                        example:
                            "MMM 'YY": [
                                ["Date", "Day", "Event", "DO", "-"]
                            ]
                            "status": "success"
    """
    try:
        key = request.headers.get('X-Access-Token')
    except:
        return jsonify({'status': 'error', 'message': 'Invalid request'})
    
    cookie = login.fetchCookies(key)
    if cookie['status'] == 'error':
        return jsonify(cookie)
    cookie = json.loads(cookie['cookie'].replace("'", "\""))

    res = calendar.fetch(cookie)
    
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)