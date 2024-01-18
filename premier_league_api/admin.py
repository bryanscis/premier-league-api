from django.contrib import admin
from .models import Teams, Managers, Fixtures, Players

admin.site.register(Teams)
admin.site.register(Managers)
admin.site.register(Fixtures)
admin.site.register(Players)