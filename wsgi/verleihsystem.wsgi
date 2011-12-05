# Activate the virtualenv
activate_this = '/home/PRJ/svn/verleihsystem/environment/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os, sys

# Add the project path to the system path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))
# Export Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'verleihsystem.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
