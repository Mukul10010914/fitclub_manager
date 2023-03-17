from django.contrib import admin
from .models import client, client_membership
# Register your models here
admin.site.register(client)
admin.site.register(client_membership)