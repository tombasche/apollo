from django.core.exceptions import ValidationError
from django.db import models
import requests

from light.utils import check_is_on

light_status = (
    ('on', 'On'),
    ('off', 'Off')
)

DEFAULT_DISCOVERY = 'http://192.168.1.1'


# Create your models here.
class Light(models.Model):

    uid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    location = models.CharField(max_length=200)
    base_url = models.CharField(max_length=200, blank=True, null=True)
    discovery_url = models.CharField(max_length=200, default=DEFAULT_DISCOVERY)
    status = models.CharField(choices=light_status, max_length=200, default='off')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        When we save, confirm that the light exists on the network.
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        resp = requests.get(self.discovery_url.format(id=self.uid))
        try:
            resp.raise_for_status()
        except Exception as ex:
            raise ValidationError(f'Light not found on the network: failed with {ex}')
        else:
            super(Light, self).save()

    def __str__(self):
        return f'{self.location}'

    def poll(self):
        """
        Sync the light status with the database
        :return:
        """
        resp = requests.get(self.discovery_url.format(id=self.uid))
        resp.raise_for_status()
        on = check_is_on(resp.json(), self.uid)
        if on:
            self.status = 'on'
        else:
            self.status = 'off'
        super(Light, self).save()

