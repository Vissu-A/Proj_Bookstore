"""
WSGI config for Bookstore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

platform = sys.platform
if platform == "win32":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.local")
elif platform in ["linux", "Linux", "ubuntu", "Ubuntu"]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.dev")

application = get_wsgi_application()
