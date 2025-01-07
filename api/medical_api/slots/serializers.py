from rest_framework import serializers
from .models import AppointmentSlot

class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'is_booked', 'video_link']
        read_only_fields = ['is_booked', 'doctor']
