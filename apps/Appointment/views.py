from apps.Appointment.models import Appointment
from apps.Appointment.serializers import AppointmentSerializer
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
       user=self.request.user
       if user.role == 'SUPER_ADMIN':
           return Appointment.objects.all()
       
       if user.role == 'BUSINESS_OWNER':
           return Appointment.objects.filter(business__owner=user)
       
       return Appointment.objects.none()
   
    def perform_create(self, serializer):
        business = serializer.validated_data["business"]
       
        if business.owner != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add appointments for this business."
            )
            
        last_appointment=Appointment.objects.filter(business=business).order_by("-id").first()
        if not last_appointment:
            appointment_code="APT001"
        else:
            last_number=int(last_appointment.appointment_code[3:])
            appointment_code=f"APT{last_number+1:03d}"
            
        
       
        serializer.save(
        appointment_code=appointment_code,
        created_by=self.request.user
    )
       
       
            
        
