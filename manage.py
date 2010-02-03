#!/usr/bin/env python
import os
from django.core.management import execute_manager
try:
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'])
    else:
        import settings # Assumed to be in the same directory.

except ValueError:
    import sys
    sys.stderr.write("Error: Can't find the file '%s' in the directory containing %r. It appears you've customized things.\nPlease check the value of DJANGO_SETTINGS_MODULE.\n" % (os.environ['DJANGO_SETTINGS_MODULE'], __file__))
    sys.exit(1)

except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
