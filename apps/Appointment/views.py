from apps.Appointment.models import Appointment
from apps.Appointment.serializers import AppointmentSerializer, BookingSerializer,BookingResponseSerializer 
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied
from rest_framework import mixins, permissions, viewsets


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
       
       if user.role == 'STAFF':
          staff=user.staff_profile  
          if staff.staff_role=="MANAGER" or staff.staff_role=="RECEPTIONIST":
              return Appointment.objects.filter(business=staff.business)
          if staff.staff_role=="STAFF":
              return Appointment.objects.filter(appointment_services__staff = staff)       
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
       
class BookingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        # 1. Validate the booking request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Create the Customer, Appointment and AppointmentService
        appointment = serializer.save()

        # 3. Serialize the newly created Appointment
        response_serializer = BookingResponseSerializer(appointment)

        # 4. Return the successful response
        return Response(response_serializer.data, status=201)

            
        
