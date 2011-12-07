# Django settings for verleihsystem project.
from conf.default import *

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'verleihsystem',                      # Or path to database file if using sqlite3.
        'USER': 'verleihsystem',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'neptun.fbe.fh-weingarten.de',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/usr/webapps/verleihsystem/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://pluto.hs-weingarten.de/verleihsystem/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = 'http://pluto.hs-weingarten.de/verleihsystem/media/admin/'

# Temporary disable LDAP auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
