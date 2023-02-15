# 8B-restapi

This repo contains a Django app that acts as a RESTful API provider to get some statistics about COVID-19 cases around the world using COVID-19 free API https://covid19api.com/

# Getting Started
```
$ git clone repo https://github.com/alfredo-c-cumbana/8B-restapi.git
$ cd 8B-restpi
$ . .venv/bin/activate
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
Application is started at
http://127.0.0.1:8000/

# Create a super user
```
cd 8B-restpi
. .venv/bin/activate
$ python manage.py createsuperuser
```

provide user details

# API Documentation
http://127.0.0.1:8000/swagger/

http://127.0.0.1:8000/redoc/

# Management Command
 ```
 $ python manage.py dailytotals domain token
 eg. $ python manage.py dailytotals http://127.0.0.1:8000 2be838e30eba3867af3d00e907
 ```
