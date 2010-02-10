# Django project settings loader
import os

if 'DJANGO_ENV' in os.environ:
    config = os.environ['DJANGO_ENV']
else:
    config = 'develop'

# Import the configuration settings file - REPLACE projectname with your project
try:
    config_module = __import__('config.%s' % config, globals(), locals(), 'ConMan')
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'config.%s.py'.\n" % config)
    sys.exit(1)

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)
