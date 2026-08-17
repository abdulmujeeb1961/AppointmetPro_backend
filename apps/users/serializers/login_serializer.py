from rest_framework import serializers
from apps.users.models import User
# from rest_framework_simplejwt import serializers as jwt_serializers
# from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() # creates a text field named username that will accept a string value from the incoming request data.
    password = serializers.CharField(write_only=True) # creates a password field that also accepts a string, but write_only=True means it will be used for input only and will not be included in the serialized output.
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        attrs['user'] = user
        
        return attrs