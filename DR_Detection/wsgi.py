"""
WSGI config for DR_Detection project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = "dr_detection.production" if "WEBSITE_HOSTNAME" in os.environ else "dr_detection.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DR_Detection.settings")

application = get_wsgi_application()
