import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apollo.settings")
django.setup()

import schedule
import time

from light.models import Light


def poll_lights():
    for light in Light.objects.all():
        light.poll()


schedule.every(3).seconds.do(poll_lights)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
