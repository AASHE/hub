[![Build Status](https://travis-ci.org/AASHE/hub.svg?branch=master)](https://travis-ci.org/AASHE/hub)
[![Coverage Status](https://coveralls.io/repos/AASHE/hub/badge.svg?branch=master&service=github)](https://coveralls.io/github/AASHE/hub?branch=master)
[![Issue Count](https://codeclimate.com/github/AASHE/hub/badges/issue_count.svg)](https://codeclimate.com/github/AASHE/hub/issues)
[![Code Climate](https://codeclimate.com/github/AASHE/hub/badges/gpa.svg)](https://codeclimate.com/github/AASHE/hub)

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

    $ pip install -r requirements.txt
    $ pip install -e .

Proceed with the actual project setup:

    $ cd hub
    $ manage.py migrate

Load the supplied organizations:

    $ psql hub < iss_organization.sql

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
