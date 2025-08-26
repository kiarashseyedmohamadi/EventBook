from django.contrib import admin
from .models import Event, Booking, Payment, Venue , Profile


admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Venue)
admin.site.register(Profile)



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'status', 'venue']
    
    fields = ['title', 'organizer', 'status', 'venue', 
              'seats_total', 'seats_left', 'start_at', 
              'end_at', 'price', 'image', 'slug']