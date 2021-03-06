ipdb
====

Django application for some ip address management

Requirements
------------

- python 2.7 and the following modules:
  - django
  - django-mptt
  - ipaddress

But you are probably better off using a vagrant box for this.

Vagrant support
---------------

This source code supports vagrant, so to get a working django environment, you can:

- Clone the source code into a new directory an chdir into it
- run "vagrant up" to build the vagrant box
- run "vagrant ssh"
- inside the vagrant box, type
  - /vagrant/vagrant_postinstall.sh
    - this should download, compile, install and prepare Python 2.7 along with virtualenv
    - it will then create a virtualenv named "django" under $HOME/django
    - and will install there: django, django-mptt, ipaddress and ipython for comfortability
  - you can re-run this script, it will only ever try to do things it hasn't achieved before
- After having done that, you can type "source $HOME/django/bin/activate" to activate the new virtualenv
- Now type "cd /vagrant" to get to your source code which is shared there
- Then either type
  - ./manage.py syncdb
    - to set up the database if not already done so
    - (do not create an admin user, it's already in the json file)
- or run
  - ./manage.py runserver 0.0.0.0:8000
    - This will also make it available on your host-machine under
      - http://127.0.0.1:8000/ip
      - or
      - http://127.0.0.1:8000/admin for the admin interface (creds: test/test)

Happy django'ing!
