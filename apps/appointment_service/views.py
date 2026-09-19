from apps.appointment_service.models import AppointmentService
from rest_framework import viewsets
from .serializers import AppointmentServiceSerializer
from rest_framework.permissions import IsAuthenticated


class AppointmentServiceViewSet(viewsets.ModelViewSet):
    
    serializer_class = AppointmentServiceSerializer
    permission_classes = [IsAuthenticated]
    queryset = AppointmentService.objects.all()

    
   