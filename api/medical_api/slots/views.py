from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AppointmentSlot
from .serializers import AppointmentSlotSerializer
from .permissions import IsDoctor, IsPatient


class AppointmentSlotListView(APIView):
    """
    Handles listing and creating appointment slots:
    - Patients can view available slots.
    - Doctors can create new slots.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, IsDoctor]
        elif self.request.method == "GET":
            self.permission_classes = [IsAuthenticated, IsPatient]
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
        List all available appointment slots.
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
        responses={201: AppointmentSlotSerializer, 400: "Bad Request"}
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


class AppointmentSlotDetailView(APIView):
    """
    Handles individual appointment slots:
    - Retrieve details for a specific slot.
    - Update or delete a slot (for doctors).
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            self.permission_classes = [IsAuthenticated, IsDoctor]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Retrieve an appointment slot by ID.",
        responses={200: AppointmentSlotSerializer, 404: "Slot not found"}
    )
    def get(self, request, slot_id):
        """
        Retrieve details of a specific appointment slot.
        """
        slot = get_object_or_404(AppointmentSlot, id=slot_id)
        serializer = AppointmentSlotSerializer(slot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update an appointment slot by ID (for doctors).",
        request_body=AppointmentSlotSerializer,
        responses={200: AppointmentSlotSerializer, 400: "Bad Request", 404: "Slot not found"}
    )
    def put(self, request, slot_id):
        """
        Update a specific appointment slot (for doctors).
        """
        slot = get_object_or_404(AppointmentSlot, id=slot_id, doctor=request.user)
        serializer = AppointmentSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an appointment slot by ID (for doctors).",
        responses={204: "Slot deleted successfully", 404: "Slot not found"}
    )
    def delete(self, request, slot_id):
        """
        Delete a specific appointment slot (for doctors).
        """
        slot = get_object_or_404(AppointmentSlot, id=slot_id, doctor=request.user)
        slot.delete()
        return Response({"detail": "Slot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
