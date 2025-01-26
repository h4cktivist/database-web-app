from django.contrib import admin

from .models import Sessions, SessionTypes, Tickets


admin.site.register(Sessions)
admin.site.register(SessionTypes)
admin.site.register(Tickets)
