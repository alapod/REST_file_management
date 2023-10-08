## Cloud file management system 
### REST API service

This is a cloud file management system. 

Prerequisites:
- Django~=4.0.3
- djangorestframework~=3.13.1
- django-mptt~=0.13.4

## To start the server:
    python manage.py runserver
   
## To run tests:
     python unit_test.py

# REST API
What you can do

## Get info about files and folders
    GET /nodes/id
  
## Import file or folder data
    POST /imports

## Delete file/folder data
    DELETE /delete/id

TODO:
- ~Idempotence~
- Exceptions in middleware
- Transactions atomicity
- Tests

