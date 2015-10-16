# Deployment to Heroku

## Deploying:

    git push heroku master

To deploy a branch other than master:

    git push heroku <branch>:master

## Running Migrations

    heroku run python manage.py migrate auth  # first migration only
    heroku run python manage.py migrate

## Buildpack configuration

We're using two buildpacks to ensure that we can run the node.js builds as well as install the python requirements.

### Reference Materials

[Using Multiple Buildpacks for an App](https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app)

[Node.js Support](https://devcenter.heroku.com/articles/nodejs-support#customizing-the-build-process)

    $ heroku buildpacks:set https://github.com/heroku/heroku-buildpack-python
    $ heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-nodejs

## Make yourself an admin:

`heroku run python manage.py shell`

    from django.contrib.auth.models import User
    u = User.objects.get(email='<your email>')
    u.is_superuser = True
    u.save()
