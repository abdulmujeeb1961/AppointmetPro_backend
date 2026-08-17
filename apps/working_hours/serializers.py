from rest_framework import serializers
from apps.working_hours.models import WorkingHours



class WorkingHoursSerializer(serializers.ModelSerializer):
    
    def validate_staff(self, value):
        request=self.context['request']
        if value.business.owner != request.user :
            raise serializers.ValidationError("You are not authorized to manage working hours for this staff member.")
        return value
        
    def validate_start_time(self, value):
        
        if value is None:
            raise serializers.ValidationError("Start time cannot be null.")
        return value
        
    
    def validate_end_time(self, value):
        if value is None:
            raise serializers.ValidationError("End time cannot be null.")
        
        return value
    
        
    def validate(self, attrs):
     staff = attrs.get("staff")
     day_of_week = attrs.get("day_of_week")
     start_time = attrs.get("start_time")
     end_time = attrs.get("end_time")

     if staff is None or day_of_week is None:
        return attrs

     queryset = WorkingHours.objects.filter(staff=staff, day_of_week=day_of_week)

     if self.instance:
        queryset = queryset.exclude(pk=self.instance.pk)

     if queryset.exists():
        raise serializers.ValidationError(
            {
                "day_of_week": f"Working hours already exist for this staff member on {day_of_week}."
            }
        )
        
     if start_time and end_time:
      if start_time >= end_time:
        raise serializers.ValidationError(
            {
                "end_time": "End time must be later than start time."
            }
        )
        
      return attrs
        
    class Meta:
        model = WorkingHours
        fields = "__all__"
        read_only_fields = ["staff", "created_at", "updated_at"]
    
     
    
    
    
      
    