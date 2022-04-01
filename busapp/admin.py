from django.contrib import admin

# Register your models here
from .models import Appointment, User, Driver, Route, Bus
admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Appointment)
admin.site.register(Bus)
