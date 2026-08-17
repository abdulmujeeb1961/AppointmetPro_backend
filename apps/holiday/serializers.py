from rest_framework import serializers
from .models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
          
    
    def validate(self, attrs):
        business=attrs.get('business')
        holiday_date=attrs.get('holiday_date')
        is_full_day = attrs.get('is_full_day')
        start_time=attrs.get('start_time')
        end_time=attrs.get('end_time')
        user=self.context['request'].user
        
        if business.owner != user:
            raise serializers.ValidationError("You are not authorized to manage this business.")
        
        if business and holiday_date:
            qs = Holiday.objects.filter(business=business, holiday_date=holiday_date)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("A holiday on this date already exists for this business.")
        
        if is_full_day:
            if start_time or end_time:
             raise serializers.ValidationError("Start time and end time cannot be provided for full day holidays.")
        else:
            if not start_time or not end_time:
                raise serializers.ValidationError("Start time and end time must be provided.")
            
            if start_time >= end_time:
              raise serializers.ValidationError(
             "Start time must be earlier than end time."
    )
            
            
                  
        return attrs

       

    
    class Meta:
        model = Holiday
        fields = '__all__'
        
        
    