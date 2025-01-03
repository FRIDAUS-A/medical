from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'medical_history', 'role', 'allergies']
        read_only_fields = ['id', 'email']

    def update(self, instance, validated_data):
        # Update the user instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
