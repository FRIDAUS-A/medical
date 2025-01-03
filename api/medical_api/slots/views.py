from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AppointmentSlot
from .serializers import AppointmentSlotSerializer
from .permissions import IsDoctor, IsPatient

class AppointmentSlotView(APIView):
    """
    Handles appointment slots:
    - Doctors can create and manage their slots.
    - Patients can view available slots for booking.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Assign permissions based on the action.
        """
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, IsDoctor]
        elif self.request.method == "GET":
            self.permission_classes = [IsAuthenticated, IsDoctor]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Get available appointment slots (for patients).",
        manual_parameters=[
            openapi.Parameter(
                'date', openapi.IN_QUERY, description="Filter slots by date (YYYY-MM-DD).", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'specialty', openapi.IN_QUERY, description="Filter slots by doctor's specialty.", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'doctor', openapi.IN_QUERY, description="Filter slots by doctor ID.", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: AppointmentSlotSerializer(many=True)}
    )
    def get(self, request):
        """
        List all available appointment slots (for patients).
        Filters:
        - By date
        - By specialty
        - By doctor
        """
        date = request.query_params.get('date')  # e.g., 2025-01-01
        specialty = request.query_params.get('specialty')  # e.g., 'cardiology'
        doctor = request.query_params.get('doctor')  # Doctor's ID
        
        slots = AppointmentSlot.objects.filter(is_booked=False, date__gte=now().date())

        # Apply filters
        if date:
            slots = slots.filter(date=date)
        if specialty:
            slots = slots.filter(doctor__specialty__icontains=specialty)
        if doctor:
            slots = slots.filter(doctor_id=doctor)

        serializer = AppointmentSlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create an appointment slot (for doctors).",
        request_body=AppointmentSlotSerializer,
        responses={
            201: AppointmentSlotSerializer,
            400: "Bad Request - Invalid data."
        }
    )
    def post(self, request):
        """
        Create an appointment slot (for doctors).
        """
        serializer = AppointmentSlotSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateAppointmentSlotView(APIView):
    """
    Allows doctors to update their existing appointment slots.
    """
    permission_classes = [IsAuthenticated, IsDoctor]
    @swagger_auto_schema(
        operation_description="Update an appointment slot. Only the doctor who created the slot can update it.",
        request_body=AppointmentSlotSerializer,
        responses={
            200: AppointmentSlotSerializer,
            400: "Bad Request",
            404: "Slot not found or unauthorized",
        },
    )
    def put(self, request, slot_id):
        """
        Update an existing appointment slot.
        """
        try:
            # Fetch the slot
            slot = AppointmentSlot.objects.get(id=slot_id, doctor=request.user)
        except AppointmentSlot.DoesNotExist:
            return Response(
                {"detail": "Appointment slot not found or unauthorized access."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize and validate the data
        serializer = AppointmentSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
