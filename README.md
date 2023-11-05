
![Logo](https://socialify.git.ci/mvishok/vcademia-api/image?description=1&descriptionEditable=An%20(Unofficial)%20API%20for%20accessing%20SRM%20Academia%20Web%20Portal%20with%0Astreamlined%20access&font=Raleway&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F89720170%3Fv%3D4&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto)


# Overview

Vcademia, an unofficial REST API, offers streamlined access to the SRM Academia portal through a Python and Flask-based system. Hosted on Vercel, the API provides endpoints for retrieving course details, student information, attendance records, marks data, timetable specifics, and calendar details. The entire project is openly accessible on GitHub, featuring Swagger documentation for easy reference. Authentication is implemented through headers using access keys and deployment is automated using GitHub Actions.

#### Objective: 
The objective of this project is to provide a REST API to access SRMIST' Academia portal. The API provides endpoints to retrieve course details, student details, attendance details, marks details, timetable details and calendar details.
## Demo
API Endpoint: `https://vcademia.api.vishok.tech/`
![Screenshot](https://raw.githubusercontent.com/mvishok/vcademia-api/main/api/media/img/screenshot.png)
## Features

- Access to the following from Academia Portal:
   - Login (Auth)
   - Course details
   - Student details
   - Attendance details
   - Marks details
   - Timetable

- Swagger Documentation



## Documentation

API Documentation is available at: https://vcademia.api.vishok.tech/


## Usage/Examples

 1. To obtain access code of a user:
```
curl -X POST "http://localhost:5000/key" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "user=netid&pass=password"
```

2. To obtain data from other endpoints:
```
#curl -X GET "http://localhost:5000/<endpoint>" -H "accept: application/json" -H "x-access-token: accesskey"
```
