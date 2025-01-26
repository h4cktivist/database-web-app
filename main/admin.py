from django.contrib import admin

from customers.models import Customers
from movies.models import Movies
from staff.models import Staff, Positions
from halls.models import Halls
from .models import Sales, Sessions, SessionTypes, Tickets


admin.site.register(Customers)
admin.site.register(Halls)
admin.site.register(Movies)
admin.site.register(Positions)
admin.site.register(Sales)
admin.site.register(SessionTypes)
admin.site.register(Sessions)
admin.site.register(Staff)
admin.site.register(Tickets)
