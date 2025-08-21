from rest_framework import serializers
from .models import Venue,Event,Booking,Payment

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_title','address','description','image']
        read_only_fields = ['slug']
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','organizer','venue','price','image']
        read_only_fields = ['slug','status','seats_total','seats_left','start_at','end_at','create_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','event','ticket_count']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking','ref','status','created_at'] 
        read_only_fields = ['booking','ref','status','created_at']
