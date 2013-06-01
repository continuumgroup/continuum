# STL Home

Helping the homeless find shelter.

## Setting up Dev

 1. get [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito)
 2. `mkvirtualenv stlhome`
 3. `workon stlhome`
 4. `pip install -r reqs/dev.txt`
 5. `python manage.py syncdb --migrate` (your option to create superuser or not)

To run the server, `python manage.py runserver`. To run a shell: `python manage.py shell`
