"""
WSGI config for qwizkoolweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

# add the django project path into the sys.path
sys.path.append('/home/vinod/work/qwizkool-django/qwizkoolweb/')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/vinod/work/qwizkool-django/.venv/lib/python3.8/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qwizkoolweb.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'qwizkoolweb.settings'

application = get_wsgi_application()

