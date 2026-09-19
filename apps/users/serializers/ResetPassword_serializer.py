from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode # for decoding the UID
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator # for verifying the token
# from django.contrib.auth.password_validation import validate_password # for validating the password This checks minimum length , common passwords , numeric passwords and similarity to username
from apps.users.models import User
import re


class ResetPasswordSerializer(serializers.Serializer):
    # Data received from the frontend
    uid = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        # Get values from request data
        uid = attrs.get("uid")
        token = attrs.get("token")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        
        if len(new_password) < 8:
            raise serializers.ValidationError(
            {"new_password": "Password must be at least 8 characters long."} )
                
        
        if re.search(r'[A-Z]', new_password) is None:
            raise serializers.ValidationError(
                {"new_password": "Password must contain at least one uppercase letter."}
            )
            
        if re.search(r'[a-z]', new_password) is None:
            raise serializers.ValidationError(
                {"new_password": "Password must contain at least one lowercase letter."}
            )
            
        if re.search(r'\d', new_password) is None:
            raise serializers.ValidationError(
                {"new_password": "Password must contain at least one digit."}
            )
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password) is None:
            raise serializers.ValidationError(
                {"new_password": "Password must contain at least one special character."}
            )
            
        if new_password != confirm_password:
             raise serializers.ValidationError(
             {"confirm_password": "Passwords do not match."})
        
        

        # Decode the UID received from the email link
        try:
            uid = force_str(urlsafe_base64_decode(uid))
        except Exception:
            raise serializers.ValidationError(
                {"uid": "Invalid password reset link."}
            )

        # Find the user using the decoded UID
        user = User.objects.filter(pk=uid).first()

        # Check whether the user exists
        if not user:
            raise serializers.ValidationError(
                {"uid": "User does not exist."}
            )

        # Prevent the user from reusing the old password
        if user.check_password(new_password):
            raise serializers.ValidationError(
                {
                    "new_password": (
                        "New password cannot be the same as the old password."
                    )
                }
            )

        # Apply Django's built-in password validators
        # validate_password(new_password, user)

        # Verify that the token is valid and has not expired
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {"token": "Invalid or expired token."}
            )

        # Store the user object so that it can be accessed in save()
        # and later in the view through serializer.validated_data["user"]
        attrs["user"] = user

        return attrs

    def save(self, **kwargs):
        # Get the validated user object
        user = self.validated_data["user"]

        # Get the validated new password
        new_password = self.validated_data["new_password"]

        # Hash and save the new password
        user.set_password(new_password)
        user.save()

        return user