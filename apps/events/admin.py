from django.contrib import admin
from .models import Event, Booking, Payment, Venue

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Venue)


