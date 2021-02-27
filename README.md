API for social network Yatube, version 2 (https://github.com/volhadounar/hw05_final.git)
=================================

A service, API to create personal posts and comments on others' records, groups for post,
the opportunity to subscribe for the users to recieve their news.  


Tools: Python3, Django Rest Framework, SQLite3, JWT Authentication,DefaultRouter,  ModelViewSet, 
GenericViewSet, Mixins, ModelSerializer, Django Filter Backend, Django Search Filter.

Getting Started
===============

1. You can build it in steps:
    1. ``cd ...wherever...``
    2. ``git clone https://github.com/volhadounar/api_final_yatube.git``
    3. ``cd api_final_yatube``
    4. ``pip install -r requirements.txt``  -- Should install everything you need
    5. ``python3 manage.py migrate`` -- Reads all the migrations folders in the application folders and creates / evolves the tables in the database
    6. ``python3 manage.py createsuperuser`` 
    7. ``python3 manage.py runserver`` -- Running localy
2. Using in Postman:
    1. POST http://localhost:8000/api/v1/token/ and pass in body request username and password:
        {"username": "my_username", "password": "my_password"}
    2. Put token in headers of request: ``Authorization: Bearer <token>``
    3. Use documentation available on ``http://localhost:8000/redoc/``
    
