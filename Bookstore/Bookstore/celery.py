from __future__ import absolute_import, unicode_literals
import os
import sys
from celery import Celery

# set the default Django settings module for the 'celery' program.
platform = sys.platform
if platform == "win32":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.local")
elif platform in ["linux", "Linux", "ubuntu", "Ubuntu"]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookstore.settings.dev")

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('Bookstore')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))