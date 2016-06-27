# Heroku Tips & Tricks

## Load a database backup from Heroku and install it locally:

1. heroku pg:backups capture
2. heroku pg:backups public-url <backup_num>  #=>backup_url
   -  get backup_num with cmd "heroku pgbackups"
3. curl -o latest.dump "<backup_url>"

Then locally do:

    $ pg_restore --verbose --clean --no-acl --no-owner \
      -h localhost -U hub -d hub latest.dump

(your database must exist before can do this)


How I do this (Ben):

    heroku pg:backups capture HEROKU_POSTGRESQL_OLIVE_URL --app aashe-hub-stage
    heroku pg:backups public-url b### --app aashe-hub-stage
    curl -o latest.dump "<backup_url>"
    
    # Rename the exiting hub database and create new DB called hub
    
    # Restore: (For some reason I have to run this twice)
    pg_restore --verbose --clean --no-acl --no-owner -h localhost -d hub latest.dump
