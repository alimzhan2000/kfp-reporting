"""
WSGI config for kfp_reporting project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')

application = get_wsgi_application()

