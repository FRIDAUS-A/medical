from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, AppointmentSlot
from .serializers import BookingSerializer
from drf_yasg.utils import swagger_auto_schema


from django.core.mail import send_mail
from django.conf import settings

def send_booking_confirmation_email(booking):
    send_mail(
        subject="Appointment Booking Confirmation",
        message=f"Dear {booking.patient.firstName + ' ' + booking.patient.last_name},\n\nYour appointment with {booking.slot.doctor.first_name + '' + booking.slot.doctor.last_name} on {booking.slot.date} at {booking.slot.start_time} has been confirmed.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.patient.email, booking.slot.doctor.email],
    )

# Inside perform_create
# send_booking_confirmation_email(serializer.instance)


class BookingView(APIView):
    """
    Handles booking creation, retrieval, and deletion.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all bookings for the authenticated user",
        responses={200: BookingSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve all bookings for the authenticated user.
        """
        bookings = Booking.objects.filter(patient=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Book an available appointment slot",
        request_body=BookingSerializer,
        responses={201: BookingSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        """
        Book an available appointment slot.
        """
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            # send_booking_confirmation_email(serializer.instance)
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a booking by ID",
        responses={204: "Booking deleted successfully", 404: "Booking not found"}
    )
    def delete(self, request, booking_id=None):
        """
        Delete a booking and free up the associated appointment slot.
        """
        booking = get_object_or_404(Booking, id=booking_id, patient=request.user)
        # Mark the slot as available
        booking.slot.is_booked = False
        booking.slot.save()
        booking.delete()
        return Response({"detail": "Booking deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
