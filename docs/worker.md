# Worker Process for the hub

We use [celery](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html) to manage background processes in the hub.

If you have redis running, then running the full application with worker should
be as easy as:

        $ heroku local

_(See notes on heroku local in docs/heroku.md)_

Most of the time, you'll want to `export CELERY_ALWAYS_EAGER=0` so that you
don't have to worry about celery and can have the tasks operate synchronously. You
really only need to do this when testing or creating tasks. This also means
that you can use the much easier:

        $ ./manage.py runserver

instead of `heroku local`.

## Redis for messages

Since it's easy and free to get redis going on heroku, I've chosen redis for
message queue.

I use homebrew to install redis:

        $ homebrew install redis

Since I don't need it running all the time, I just start it as needed:

        $ redis-server /usr/local/etc/redis.conf

Redis is available for free from heroku:

        $ heroku addons:create heroku-redis:hobby-dev

## Worker Result Storage

Right now, since we're just using this for thumbnailing, we don't have a use
for the result store, but if we do then we'll probably want to install
[django-celery](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-django-orm-cache-as-a-result-backend) and add a backend.
