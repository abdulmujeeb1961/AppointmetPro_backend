from rest_framework import serializers
from apps.customer.models import Customer
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
        read_only_fields = ["created_at", "updated_at"]
        
    def validate_business(self,value):    
        request=self.context['request']
        if value.owner != request.user :
            raise serializers.ValidationError("You are not authorized to manage this business.")
        return value
    
    def validate_first_name(self,value) :
        value=value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("First name must have at least 2 characters.")
        
        if not value.replace(" ","").isalpha():
            raise serializers.ValidationError("First name must contain only characters.")
        return value
    
    def validate_last_name(self, value):
     value = value.strip()

     if value:
        if len(value) < 2:
            raise serializers.ValidationError(
                "Last name must have at least 2 characters."
            )

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Last name must contain only characters."
            )

     return value
             
    def validate_mobile_number(self,value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits long.")
        if not value.startswith(('9', '8' , '6', '7')):
            raise serializers.ValidationError("Mobile number must start with '9,8,6,7'.")
        return value
    def validate_date_of_birth(self,value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth must not be greater than current date")
        return value
    def validate_anniversary_date(self,value):
        if value > date.today():
            raise serializers.ValidationError("Anniversary date must not be greater than current date")
        return value
    
    def validate_address(self,value):
        if value:
            value=value.strip()
        return value
        
    
    def validate_notes(self,value):
        if value:
            value=value.strip()
        return value
    
    def validate(self,attrs):
        
        business=attrs.get('business')
        first_name=attrs.get('first_name')
        last_name=attrs.get('last_name')
        mobile_number=attrs.get('mobile_number')
        
        queryset=Customer.objects.filter(business=business,first_name=first_name,last_name=last_name,mobile_number=mobile_number)
        
        if self.instance:
            queryset=queryset.exclude(pk=self.instance.pk)
            
        
        if queryset.exists():
         raise serializers.ValidationError(
            {
                "mobile_number" : 
                f"Mobile Number {mobile_number} is already registered for a customer with the same name in this business"
            })
        return attrs
        
        
  
                    
                       
        
        
        
        
