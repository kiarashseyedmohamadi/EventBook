from rest_framework import serializers
from .models import Venue,Event,Booking,Payment,User

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_title','address','description','image']
        read_only_fields = ['slug']
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','organizer','venue','price','image','seats_total','seats_left']
        read_only_fields = ['slug','status','start_at','end_at','create_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','event','ticket_count']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking','ref','status','created_at'] 
        read_only_fields = ['booking','ref','status','created_at']

#================================================================================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password")
        

#--------

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


#--------  

class VerifyCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=5)
     
    