from django.urls import path
from .import views


app_name='events'

urlpatterns = [
     path('',views.TestAPIView.as_view(), name='register'),
]
