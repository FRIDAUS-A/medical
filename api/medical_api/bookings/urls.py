from django.urls import path
from .views import BookingView

urlpatterns = [
    path('bookings/', BookingView.as_view(), name='bookings'),
    path('bookings/<str:booking_id>/', BookingView.as_view(), name='delete-booking'),
]
