from django.contrib import admin

# Register your models here.
from light.models import Light

admin.site.register(Light)

class LightAdmin(admin.ModelAdmin):
    change_form_template = 'templates/admin/light/light/change_form.html'