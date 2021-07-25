#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    platform = sys.platform
    if platform == "win32":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.local")
    elif platform in ["linux", "Linux", "ubuntu", "Ubuntu"]:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.dev")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
