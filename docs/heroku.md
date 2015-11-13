# Heroku Tips & Tricks

## Load a database backup from Heroku and install it locally:

1. heroku pgbackups:capture
2. heroku pgbackups:url <backup_num>  #=>backup_url
   -  get backup_num with cmd "heroku pgbackups"
3. curl -o latest.dump <backup_url>

Then locally do:

    $ pg_restore --verbose --clean --no-acl --no-owner \
      -h localhost -U hub -d hub latest.dump

(your database must exist before can do this)
