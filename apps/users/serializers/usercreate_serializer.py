from apps.users.models import User
from rest_framework import serializers
import re


class UserCreateSerializer(serializers.ModelSerializer):

    # Password is accepted from the frontend but will never
    # be returned in the API response.
    password = serializers.CharField(write_only=True)

    # confirm_password is not a database field.
    # It is used only to check that both passwords match.
    confirm_password = serializers.CharField(write_only=True)

    # Last name is optional and blank value is allowed.
    last_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # Email is optional, not unique, and blank value is allowed.
    # DRF will still check email format if an email is supplied.
    email = serializers.EmailField(
        required=False,
        allow_blank=True
    )

    # ---------------------------------------------------------
    # FIRST NAME VALIDATION
    # ---------------------------------------------------------

    def validate_first_name(self, value):

        # Remove leading and trailing spaces.
        value = value.strip()

        # First name cannot be empty.
        if not value:
            raise serializers.ValidationError(
                "First name is required"
            )

        # First name must contain at least 2 characters.
        if len(value) < 2:
            raise serializers.ValidationError(
                "First name must be at least 2 characters long"
            )

        # Allow alphabets and spaces only.
        # replace() removes spaces before checking isalpha().
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "First name must contain only characters"
            )

        return value

    # ---------------------------------------------------------
    # USERNAME VALIDATION
    # ---------------------------------------------------------

    def validate_username(self, value):

        # Remove leading and trailing spaces.
        value = value.strip()

        # Username cannot be empty.
        if not value:
            raise serializers.ValidationError(
                "Username is required"
            )

        # Username must contain at least 3 characters.
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long"
            )

        # Username must contain alphanumeric characters.
        if not value.replace(" ", "").isalnum():
            raise serializers.ValidationError(
                "Username must contain only alphanumeric characters"
            )

        # Check whether the username already exists.
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )

        return value

    # ---------------------------------------------------------
    # MOBILE NUMBER VALIDATION
    # ---------------------------------------------------------

    def validate_mobile_number(self, value):

        # Mobile number must contain digits only.
        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        # Mobile number must contain exactly 10 digits.
        if len(value) != 10:
            raise serializers.ValidationError(
                "Mobile number must be 10 digits long."
            )

        # Indian mobile numbers should start with 6, 7, 8 or 9.
        if not value.startswith(('6', '7', '8', '9')):
            raise serializers.ValidationError(
                "Mobile number must start with 6, 7, 8, or 9."
            )

        return value

    # ---------------------------------------------------------
    # ROLE VALIDATION
    # ---------------------------------------------------------

    def validate_role(self, value):

        # Remove leading and trailing spaces.
        value = value.strip()

        # Role cannot be empty.
        if not value:
            raise serializers.ValidationError(
                "Role is required"
            )

        # Only these three roles are allowed.
        if value not in [
            'SUPER_ADMIN',
            'BUSINESS_OWNER',
            'STAFF'
        ]:
            raise serializers.ValidationError(
                "Role must be SUPER_ADMIN, BUSINESS_OWNER, or STAFF"
            )

        return value

    # ---------------------------------------------------------
    # PASSWORD AND CONFIRM PASSWORD VALIDATION
    # ---------------------------------------------------------

    def validate(self, attrs):

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Password is mandatory.
        if password is None:
            raise serializers.ValidationError(
                "Password is required"
            )

        # Password must contain at least 8 characters.
        if len(password) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )

        # Password must contain at least one uppercase letter.
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter"
            )

        # Password must contain at least one lowercase letter.
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter"
            )

        # Password must contain at least one digit.
        if not re.search(r'\d', password):
            raise serializers.ValidationError(
                "Password must contain at least one digit"
            )

        # Password must contain at least one special character.
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError(
                "Password must contain at least one special character"
            )

        # Confirm password is mandatory.
        if not confirm_password:
            raise serializers.ValidationError(
                "Confirm password is required"
            )

        # Both passwords must be identical.
        if password != confirm_password:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return attrs

    # ---------------------------------------------------------
    # CREATE USER
    # ---------------------------------------------------------

    def create(self, validated_data):

        # confirm_password is only for validation.
        # It does not exist in the User model.
        validated_data.pop('confirm_password')

        # Remove the plain password temporarily.
        password = validated_data.pop('password')

        # Create User object with the remaining fields.
        user = User(**validated_data)

        # Convert the plain password into Django's secure
        # password hash before saving it to the database.
        user.set_password(password)

        # Save the user in the database.
        user.save()

        return user

    # ---------------------------------------------------------
    # MODEL CONFIGURATION
    # ---------------------------------------------------------

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'mobile_number',
            'role',
            'password',
            'confirm_password',
        ]