import sys, os

PROJECT_ROOT = '/home/unitestm/depth2'
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jurnal_poc.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()