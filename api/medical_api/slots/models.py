from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class AppointmentSlot(models.Model):
    id = models.CharField(max_length=50, primary_key=True, blank=False,  default=uuid.uuid4())
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)  # To track if a slot is booked
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time} - {self.end_time}"
