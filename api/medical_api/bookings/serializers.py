from rest_framework import serializers
from .models import Booking, AppointmentSlot

class BookingSerializer(serializers.ModelSerializer):
    slot_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'patient', 'slot', 'slot_id', 'created_at']
        read_only_fields = ['id', 'patient', 'slot', 'created_at']

    def validate_slot_id(self, value):
        try:
            slot = AppointmentSlot.objects.get(id=value, is_booked=False)
            return slot
        except AppointmentSlot.DoesNotExist:
            raise serializers.ValidationError("The selected slot is either invalid or already booked.")

    def create(self, validated_data):
        slot = validated_data.pop('slot_id')
        validated_data['slot'] = slot
        validated_data['patient'] = self.context['request'].user
        slot.is_booked = True  # Mark the slot as booked
        slot.save()
        return super().create(validated_data)
