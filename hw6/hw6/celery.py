import os
from celery import Celery
from homm3_creatures.tasks import creatures_counter

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw6.settings')
app = Celery('hw6')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
    'task': 'homm3_creatures.tasks.creatures_counter',
    'schedule': 60.0,
    'args': ()},
}
app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')