from rest_framework import serializers
from apps.services.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(
        source="business.business_name",
        read_only=True)
    
    def validate_service_name(self,value):
        # Validation for service_name
        if len(value.strip()) <3: # strip has been used to delete trailing spaces
            raise serializers.ValidationError("Service name must have atleast 3  characters.")
        return value.strip()
        
               
    def validate_duration_minutes(self,value):
        if value < 1 or value  > 720:
            raise serializers.ValidationError("Duration must be greater than 0 and less than 720.")
        return value
        
    def validate_price(self,value):
        if value <= 0 :
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
        
    def validate_display_order(self,value):
        if value < 1 :
            raise serializers.ValidationError("Display order must be greater than 0.")
        
        return value
    

    def validate(self,attrs):
        business = attrs.get("business")
        
        service_name = attrs.get("service_name").strip() # strip has been used to delete trailing spaces

    # Save the cleaned name back
        attrs["service_name"] = service_name
        if self.instance and self.instance.service_name == service_name and self.instance.business == business: 
            return attrs  # No change in service_name or business, so no need to check for duplicates
        

    # Check duplicate within the same business and is case insensative. e.g Hair Cut and hair cut will be treated as same.  __iexact is used for case insensitivity
        if Service.objects.filter(
        business=business,
        service_name__iexact=service_name
    ).exists():
         raise serializers.ValidationError(
            {
                "service_name": "A service with this name already exists for this business."
            }
        )

        return attrs
    
    
    
    
    
    
    class Meta:
        model = Service
        fields = [
            "id",
            "business",
            "business_name",
            "service_name",
            "duration_minutes",
            "price",
            "display_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at","business_name"]