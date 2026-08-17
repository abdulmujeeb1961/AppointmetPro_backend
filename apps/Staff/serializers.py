from rest_framework import serializers
from apps.Staff.models import Staff
from datetime import date




class StaffSerializer(serializers.ModelSerializer):
    
    # def validate_business(self, value):
    #     if value.owner != self.context['request'].user:
    #         raise serializers.ValidationError("You are not the owner of this business")
    #     return value
    
    def validate_first_name(self, value):
        value=value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("First name must have at least 2 characters.")
        if not value.replace(" ","").isalpha():
            raise serializers.ValidationError("First name must contain only characters.")
        return value
    
    def validate_last_name(self, value):
            value=value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("Last name must have at least 2 characters.")
            if not value.replace(" ","").isalpha():
                raise serializers.ValidationError("Last name must contain only characters.")
            return value
        
    def validate_mobile_number(self,value):
        value=value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits long.")
        if not value.startswith(('9', '8' , '6', '7')):
            raise serializers.ValidationError("Mobile number must start with '9,8,6,7'.")
        return value
    
    def validate_designation(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Designation must have at least 2 characters.")
        return value.strip()
    
    def validate_joining_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Joining date cannot be  future date.")
        return value
    
    def validate_experience_years(self,value):
        if value < 0 or value > 60:
            raise serializers.ValidationError("Experience years must be between 0 and 60.")
        return value
    
    def validate_notes(self,value):
        if value :
            value=value.strip()
        return value
    
    
        
    
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ["staff_code","created_at", "updated_at"]
        
    
    
    