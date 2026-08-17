from apps.business.models import Business
from rest_framework import serializers
import re

class BusinessSerializer(serializers.ModelSerializer):
            
        
        
        def validate_mobile_number(self, value): # here self will be the instance i.e. max_length etc whereas value will have the actual value i.e. mobile_number.
            if not value.isdigit():
                raise serializers.ValidationError("Mobile number must contain only digits.")
            if len(value) != 10:
                raise serializers.ValidationError("Mobile number must be 10 digits long.")
            if not value.startswith(('9', '8' , '6', '7')):
                raise serializers.ValidationError("Mobile number must start with '9,8,6,7'.")
            return value
            
        def validate_gst(self, value):
             if not value:
                 return value # this is done as the filed is not mandatory and if the value is empty we will return it as it is.

             value = value.strip().upper() # removing spaces and converting to uppercase

             gst_pattern = r'^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$' # this pattern starts with 2 digits, followed by 5 characters (A-Z), followed by 4 digits, followed by 1 character (A-Z), followed by 1 character (1-9A-Z), followed by Z, followed by 1 character (A-Z). This starts with r'^ and ends with $'. For digtes we have \d followed by the number within{} and for characters we have [A-Z] followed by the number within {}.

             if not re.match(gst_pattern, value):
                 raise serializers.ValidationError(
            "Enter a valid GST number. Example: 27ABCDE1234F1Z5"
        )

             return value
        
        def validate_pan(self,value):
            if not value:
                return value
            if len(value) != 10:
               raise serializers.ValidationError("PAN number must be 10 digits long.")
           
            if not value[:5].isalpha():
                raise serializers.ValidationError("First five PAN number must contain only characters.")
            if not value[5:9].isdigit(): 
                raise serializers.ValidationError("After first 5 appha caracters next four PAN number must contain only digits.")
            if not value[9].isalpha():
                raise serializers.ValidationError("Last character must be alpha")
            
            return value
            
        def validate_pincode(self,value):
            if not value.isdigit():
                raise serializers.ValidationError("Pincode must contain only digits.")
            if len(value) != 6:
                raise serializers.ValidationError("Pincode must be 6 digits long.")
            return value
        
        def validate_business_name(self,value):
            if len(value.strip()) <3:
                raise serializers.ValidationError("Business name must have atleast 3  characters.")
            return value
        
        class Meta:
            model = Business
            fields = '__all__'
            read_only_fields = ["owner","created_at", "updated_at"]        
            
            

        