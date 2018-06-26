import requests
from django.http import HttpResponseRedirect
from django.urls import reverse

from light.models import Light


def flip_status(request, object_pk):

    light = Light.objects.get(pk=object_pk)
    if light.status == 'on':
        target_value = 0
    else:
        target_value = 1
    resp = requests.post(light.base_url.format(id=light.uid, target_value=target_value))
    resp.raise_for_status()

    light_response = resp.json()
    if light_response.get('u:SetTargetResponse'):
        if light.status == 'on':
            light.status = 'off'
        else:
            light.status = 'on'
        light.save()
    return HttpResponseRedirect(
       reverse('admin:light_light_change', args=[object_pk])
    )
