import os
from settings import SITE_ROOT
# Django settings for conman project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Clint Savage', 'clint@utos.org'),
    ('Will Smith','undertakingyou@gmail.com'),
    ('Adam Barrett','utahcon@utahcon.com'),
)

MANAGERS = (
    ('Papers Managers', 'papers@utos.org'),
)

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'EVENTREV'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'eventrev'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'public/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e%k-fbsx3!2l&6(zjuf#f-$j95@*&o*4*9d7x4))e!%-g!att$'

import common
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'common.templateloader.load_template_source',
#    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.CacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'common.middleware.SiteIdOnFlyMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # common/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, "public/themes"),
)

INSTALLED_APPS = (
    'django.contrib.flatpages',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'common',
    'accounts',
    'speakers',
    'volunteers',
    'voting',
    'sponsors',
    'lugs',
    'updates',
    'ticketing',
    'event',
    #'locations',
    #'django.contrib.databrowse',

    # third-party apps

    # wget http://sorl-thumbnail.googlecode.com/files/sorl-thumbnail-3.2.5.tar.gz -O /tmp/sorl-thumbnail.tar.gz && \ 
    # tar xf /tmp/sorl-thumbnail.tar.gz -C /tmp && cd /tmp/sorl-thumbnail-3.2.5/ && python setup.py install
    'sorl.thumbnail',
    #useful migrations tool -- http://south.aeracode.org/
    #'south',
)

###########NEW CHANGE TO ADD###########
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request'
)
######################################

AUTH_PROFILE_MODULE = 'common.userprofile'

HOST_NAME = 'http://localhost:8080'

# UTOS-ConMan specific settings
# for sending mail to speakers.

# if you want to actually send mail, set this to True
# otherwise, just look in the output of the django
# manage.py runserver command

SEND_EMAIL = False
DEFAULT_FROM_EMAIL = 'papers@utos.org'
EMAIL_HOST = 'localhost.localdomain'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[conman-papers] '
SERVER_EMAIL = 'admin@utos.org'

FONT_PATH = os.path.join(SITE_ROOT, "public/fonts/DejaVuLGCSerifCondensed.ttf")
#FONT_PATH="arial.pil"
FONT_SIZE = 14
# Timeout in minutes
TIMEOUT = 15

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

ACCOUNT_ACTIVATION_DAYS = 3

PRESENTATION_DELETED='The presentation has been deleted.'

# social media is pretty important these days.
# including settings for twitter for now
# facebook, identi.ca and others to come.
# this depends on the the python-twitter
# set of libraries.  They can be checked out at
# http://python-twitter.googlecode.com/svn/trunk/

# PING FM
# THIS IS THE REAL ONE!!!
#PINGFM_APP_KEY = 'c982322d92d0a5b59a5db8dcb2373c76'
#PINGFM_USER_KEY = '6ac23d3f50955af53d1a0238fad4727a-1234110993'

#TESTING ACCOUNT
PINGFM_APP_KEY = 'ffe126487a69e4e920a0629cc4778c5b'
PINGFM_USER_KEY = 'eb029e56b271f687fe0bd853c7d04cf3-1251257314'

PINGFM_ENABLED = True
PINGFM = 'http://api.ping.fm/v1/'

# ALL_CAN_VOTE
# This allows anyone who signs up to become part of a special group
# called Voter (which must be in the Auth -> Groups in the admin with
ALL_CAN_VOTE = True

#memcached detail
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

#increase the file upload size to 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10

# Google API Key
GOOGLE_API_KEY = 'ABQIAAAAijiXc0gXuV9OSToAhQ6vfxTSDpTFJAVlOsTRzC7LuycYmlY3rxQ8Ytzr1XMe_od7B3qvBPb0JFGKtQ'
