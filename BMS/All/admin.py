from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Time)
admin.site.register(Inventory)
admin.site.register(Layout)
admin.site.register(User)
admin.site.register(Booking)