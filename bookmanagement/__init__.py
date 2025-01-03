from __future__ import absolute_import, unicode_literals

# This ensures that the app is always imported when Django starts,
# so that shared_task will use this app.
from library.celery import app as celery_app

__all__ = ('celery_app',)