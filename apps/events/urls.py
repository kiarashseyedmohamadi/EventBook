from django.urls import path
from .import views


app_name='events'

urlpatterns = [
     path('',views.TestAPIView.as_view(), name='register1'),
     
     # Venue
     path('venues/', views.VenueView.as_view(), name='venue-list'),  
     path('venues/<int:pk>/', views.VenueView.as_view(), name='venue-detail'), # PUT, PATCH, DELETE

     # Event
     path('events/', views.EventView.as_view(), name='event-list'),           # GET و POST
     path('events/<int:pk>/', views.EventView.as_view(), name='event-detail'), # PUT, PATCH, DELETE

     # Booking
     path('bookings/', views.BookingView.as_view(), name='booking-list'),        # GET و POST
     path('bookings/<int:pk>/', views.BookingView.as_view(), name='booking-detail'), # DELETE

     # Payment
     path('payments/<int:pk>/', views.PaymentView.as_view(), name='payment'),        # GET و POST
     
     path('register/',views.RegisterView.as_view(),name = 'register'),
     path('register/<int:id>/', views.RegisterView.as_view(), name='register-detail'),
     
     path('login/',views.LoginView.as_view(), name ='login'),
     path('verify-code/',views.VerifyCodeView.as_view(), name ='verify-code')
          
]
