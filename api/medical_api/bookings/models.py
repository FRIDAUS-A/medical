from django.db import models
from django.conf import settings
from slots.models import AppointmentSlot
import uuid

class Booking(models.Model):
    id = models.CharField(max_length=50, primary_key=True, blank=False,  default=uuid.uuid4())
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE, related_name="booking")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.patient} for slot {self.slot}"
