from django.urls import path
from .views import AppointmentSlotView
from .views import UpdateAppointmentSlotView

urlpatterns = [
    path('appointment-slots/', AppointmentSlotView.as_view(), name='appointment-slots'),
    path('appointment-slots/<str:slot_id>', UpdateAppointmentSlotView.as_view(), name='update-appointment-slots'),
]
