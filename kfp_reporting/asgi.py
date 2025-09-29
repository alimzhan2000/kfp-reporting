"""
ASGI config for kfp_reporting project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')

application = get_asgi_application()

