```
                 _            _           _
  __ _  __ _ ___| |__   ___  | |__  _   _| |__
 / _` |/ _` / __| '_ \ / _ \ | '_ \| | | | '_ \
| (_| | (_| \__ \ | | |  __/ | | | | |_| | |_) |
 \__,_|\__,_|___/_| |_|\___| |_| |_|\__,_|_.__/
```

# The Campus Sustainability Hub

## Installation, Quick'n'dirty

Install the requirements and create a blank database, migrate all the tables:

    $ pip install -e requirements.txt
    $ mysql -uroot -e'create database hub;'
    $ manage.py migrate

Load the supplied organizations:

    $ mysql -uroot hub < ~/Desktop/iss10-6-15.sql

Create a superuser to get access to the admin:

    $ manage.py createsuperuser
