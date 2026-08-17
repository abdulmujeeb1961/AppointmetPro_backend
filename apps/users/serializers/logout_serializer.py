from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid refresh token")
       
        return attrs