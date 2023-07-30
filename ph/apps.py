from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    from . import tasks  # import tasks here to avoid a circular import issue
    scheduler = BackgroundScheduler()
    scheduler.add_job(tasks.atualiza_host_sched, 'interval', minutes=2)
    scheduler.start()


class PhConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ph'

    def ready(self):
        start_scheduler()


