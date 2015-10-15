```
                 _            _           _
  __ _  __ _ ___| |__   ___  | |__  _   _| |__
 / _` |/ _` / __| '_ \ / _ \ | '_ \| | | | '_ \
| (_| | (_| \__ \ | | |  __/ | | | | |_| | |_) |
 \__,_|\__,_|___/_| |_|\___| |_| |_|\__,_|_.__/
```

# The Campus Sustainability Hub

## Installation, for local development

Copy the sample settings file and adjust the settings according to your needs:

    $ cp hub/settings/local.py.example hub/settings/local.py

Install the requirements and create a blank database, migrate all the tables:

    $ pip install -e requirements.txt
    $ mysql -uroot -e'create database hub;'
    $ manage.py migrate

Load the supplied organizations:

    $ mysql -uroot hub < ~/Desktop/iss10-6-15.sql

Create a superuser to get access to the admin:

    $ manage.py createsuperuser


## Change CSS (Compile SCSS files)

You have to install Node/npm, on a Mac:

    $ brew install node

Install the Javascript dependencies (such as sass):

    $ cd hub/
    $ npm install

Make changes to the SCSS files in `hub/static/scss` and before commit compile
them to CSS:

    $ npm run makecss
