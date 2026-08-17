from rest_framework import serializers
from .models import AppointmentService


class AppointmentServiceSerializer(serializers.ModelSerializer):

    def validate_appointment(self, attrs):
        request = self.context["request"]
        if attrs.business.owner != request.user:
            raise serializers.ValidationError(
                "You are not authorized to manage this business."
            )
        return attrs

    def validate_service(self, value):
        request = self.context["request"]
        if value.business.owner != request.user:
            raise serializers.ValidationError(
                "You are not authorized to manage this business."
            )
        return value

    def validate_staff(self, value):
        request = self.context["request"]
        if value.business.owner != request.user:
            raise serializers.ValidationError(
                "You are not authorized to manage this business."
            )
        return value

    def validate(self, attrs):
        staff = attrs.get("staff")
        service = attrs.get("service")
        appointment = attrs.get("appointment")
        scheduled_start = attrs.get("scheduled_start")
        scheduled_end = attrs.get("scheduled_end")
        actual_start = attrs.get("actual_start")
        actual_end = attrs.get("actual_end")
        print(staff.pk)
        print(service.pk)
        print(appointment.pk)
        

        if scheduled_start >= scheduled_end:
            raise serializers.ValidationError(
                "Scheduled Start time must be before Scheduled end time. "
            )

        if actual_start and actual_end:
            if actual_start >= actual_end:
                raise serializers.ValidationError(
                    "Actual start time must be before actual end time."
                )
                
        if not staff.services.filter(pk=service.pk).exists():
          raise serializers.ValidationError(
        "This staff member is not assigned to provide this service."
               )
          
        if (
        appointment.business.pk != service.business.pk
        or appointment.business.pk != staff.business.pk
    ):
         raise serializers.ValidationError(
            "The appointment, service and staff member must belong to the same business."
        )
        return attrs
    
    

    class Meta:
        model = AppointmentService
        fields = "__all__"
