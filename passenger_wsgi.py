import os
import sys

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJ_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jurnal_poc.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()