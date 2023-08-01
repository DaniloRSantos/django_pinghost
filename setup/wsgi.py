"""
WSGI config for setup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler
from ph import tasks
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

scheduler = BackgroundScheduler()
scheduler.add_job(tasks.atualiza_host_sched, 'interval', minutes=settings.INTERVAL_MINUTES, id='atualiza_host_sched')
scheduler.start()

application = get_wsgi_application()

