from django.urls import path
from .views import AppointmentSlotListView, AppointmentSlotDetailView

urlpatterns = [
    path('appointment-slots/', AppointmentSlotListView.as_view(), name='appointment-slot-list'),
    path('appointment-slots/<str:slot_id>/', AppointmentSlotDetailView.as_view(), name='appointment-slot-detail'),
]
