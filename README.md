# Continuum

Helping the homeless find shelter.

## Setting up Dev

First, you'll need to make sure you have your database set up. We need to use
postgresql in dev for geospatial queries. If you're on Mac, try
[Postgres.app][pg.app]. If you're on linux, get the latest version from your package manager.

 1. get [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito)
 1. `mkvirtualenv continuum`
 1. `workon continuum`
 1. `pip install -r reqs/dev.txt`

To enable testing, we need the `continuum` user as a superuser in the database:

    CREATE USER continuum;
    CREATE DATABASE continuum;
    ALTER USER continuum WITH superuser;

We need the btree-GiST, cube, and earthdistance extensions. They are included
in [postgres.app][pg.app], but may not be in a package manager. Try this to
make sure they're available:

    CREATE EXTENSION btree_gist;
    CREATE EXTENSION cube;
    CREATE EXTENSION earthdistance;

after you've done all this, run `python manage.py syncdb --migrate` (your
option to create superuser or not)

To run the server, `python manage.py runserver`. To run a shell: `python manage.py shell`

[pg.app]: http://postgresapp.com/ "Postgres.app"
