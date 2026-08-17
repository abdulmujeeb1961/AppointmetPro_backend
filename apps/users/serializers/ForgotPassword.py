from rest_framework import serializers
from apps.users.models import User


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        # Get email from request data
        email = attrs.get("email")

        # Find the user using email
        user = User.objects.filter(email=email).first()

        # Check if user exists
        if not user:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."}
            )

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError(
                {"email": "User account is inactive."}
            )

        # Store the User object in attrs
        attrs["user"] = user

        return attrs