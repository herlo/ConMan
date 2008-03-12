#!/usr/bin/env python
import os
import sys
from optparse import OptionParser

INDENTCOUNT = 4
INDENTCHAR = ' '

parser = OptionParser()
parser.add_option('-a', '--app', dest='app', help='The app which contains the model.')
parser.add_option('-m', '--model', dest='model', help='The model to produce the Form for.')
parser.add_option('-p', '--path', dest='path', help='The path to look for the files, directories separated by space.')
parser.add_option('-w', '--write', dest='file', help='The output file to append the form to, without this argument the output is printed.')

options, args = parser.parse_args()

if not(options.model and options.app):
    parser.print_help()
    sys.exit()

if options.path:
    sys.path += options.path.split()

if options.file:
    sys.stdout = file(options.file, 'a')

try:
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'])
    else:
        import settings
except ImportError:
    print 'Settings file not found. Place this file in the same dir as manage.py or use the path argument.'
    sys.exit()

project_directory = os.path.dirname(settings.__file__)
project_name = os.path.basename(project_directory)

sys.path.append(os.path.join(project_directory, '..'))
project_module = __import__(project_name)
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project_name
from django.newforms import form_for_model

models = __import__('%s.%s.models' % (project_name, options.app,), '', '', [options.model])
model = getattr(models, options.model)

fields = model._meta.fields + model._meta.many_to_many

print 'class %sForm(forms.Form):' % (options.model)
for field in fields:
    formfield = field.formfield()
    if formfield:
        fieldtype = str(formfield).split()[0].split('.')[-1]
        arguments = {}
        arguments['verbose_name'] = '\'%s\'' % field.verbose_name
        arguments['help_text'] = '\'%s\'' % field.help_text
        arguments['required'] = not field.blank

        print '%s%s = forms.%s(%s)' % (INDENTCOUNT * INDENTCHAR, field.name, fieldtype, ', '.join(['%s=%s' % (k, v) for k, v in arguments.iteritems()]))

