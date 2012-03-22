import os, sys
sys.path.append('/home/apache2/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'drivertab.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

