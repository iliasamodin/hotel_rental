# Booking
Hotel reservation services have been in great demand among travelers and tourists for more than twenty years. 
The author of this repository, like many, has repeatedly used the services of such sites and applications. 
This fact, among others, influenced the choice of the specifics of this educational project.

## Hotel Rental backend
This repository contains the backend of the hotel reservation application with Fastapi framework in a layer of requests 
and SQLAlchemy in the DAO layer. 
Redis is used to caching answers to user's requests, 
and Celery is used to send notifications about bookings to user's email and for warm up the cache. 
All endpoints of the application are covered with system tests, 
important components of the application are additionally covered with unit tests. 
For all tests, Pytest was used. 
The application provides for the connection of Sentry for monitoring errors in the application. 
For deployment of the application and auxiliary services, the docker-compose file is prepared.

## Why was this project written
The target of writing the project was to study and strengthen competencies of use FastAPI framework 
for processing client requests 
and SQLAlchemy library to connect and work with the DBMS from the application. 
And also improving skills of use Redis and Celery for caching and background tasks, 
Pytest for automation of the application testing and Sentry for monitoring errors.