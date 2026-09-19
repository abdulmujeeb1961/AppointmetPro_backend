from rest_framework import serializers
from apps.users.models import User


class ForgotPasswordSerializer(serializers.Serializer):
    # email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        # Get email from request data
        # email = attrs.get("email")
        username=attrs.get("username")
        

        # Find the user using email
        user = User.objects.filter(username=username).first()
         # Assuming username is unique and used for login

        # Check if user exists
        if not user:
            raise serializers.ValidationError(
                {"username": "User with this username does not exist."}
            )

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError(
                {"email": "User account is inactive."}
            )

        # Store the User object in attrs
        attrs["user"] = user

        return attrs