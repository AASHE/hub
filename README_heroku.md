# Deployment to Heroku

Deploying:

    git push heroku master

To deploy a branch other than master:

    git push heroku <branch>:master

Running Migrations

    heroku run python manage.py migrate auth  # first migration only
    heroku run python manage.py migrate

Make yourself an admin:

`heroku run python manage.py shell`

    from django.contrib.auth.models import User
    u = User.objects.get(email='<your email>')
    u.is_superuser = True
