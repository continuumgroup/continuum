# Continuum

Helping the homeless find shelter.

## Setting up Dev

 1. get [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito)
 2. `mkvirtualenv continuum`
 3. `workon continuum`
 4. `pip install -r reqs/dev.txt`
 5. `python manage.py syncdb --migrate` (your option to create superuser or not)

To run the server, `python manage.py runserver`. To run a shell: `python manage.py shell`
