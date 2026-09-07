from rest_framework import serializers
from .models import User, PendingRegistration, PrivacySettings

import phonenumbers
from phonenumbers import NumberParseException, COUNTRY_CODE_TO_REGION_CODE
import re


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
    )

    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        model = PendingRegistration

        fields = [
            "name",
            "email",
            "country_code",
            "phone_number",
            "password",
            "confirm_password"
        ]

    def validate_name(self, value):
        return value.strip()

    def validate_email(self, value):

        value = value.strip().lower()

        # Already registered user
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email is already registered."
            )

        # Registration already waiting for OTP
        if PendingRegistration.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Registration is already pending OTP verification."
            )

        return value

    def validate_phone_number(self, value):

        value = value.strip()

        return value

    def validate(self, attrs):

        country_code = attrs.get("country_code")
        phone_number = attrs.get("phone_number")

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        # Password confirmation
        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
            
        # Phone number validation

        regions = phonenumbers.country_code_for_region

        try:

            country_code_int = int(country_code)

            regions = COUNTRY_CODE_TO_REGION_CODE[
                country_code_int
            ]

            region = regions[0]

            parsed_number = phonenumbers.parse(
                phone_number,
                region
            )

        except (NumberParseException, KeyError, ValueError):

            raise serializers.ValidationError({
                "phone_number": "Invalid phone number."
            })


        # Check whether phone number is valid
        if not phonenumbers.is_valid_number(parsed_number):

            raise serializers.ValidationError({
                "phone_number": "Invalid phone number for selected country."
            })

        # Check duplicate phone number
        
        if User.objects.filter(
            country_code=country_code,
            phone_number=phone_number
        ).exists():

            raise serializers.ValidationError({
                "phone_number": "Phone number is already registered."
            })

        if PendingRegistration.objects.filter(
            country_code=country_code,
            phone_number=phone_number
        ).exists():

            raise serializers.ValidationError({
                "phone_number": "Phone number is already pending OTP verification."
            })

        return attrs
    def validate_password(self, value):

        errors = []

        if len(value) < 8 or len(value) > 20:
            errors.append(
                "Password must be 8-20 characters long."
            )

        if not re.search(r"[A-Z]", value):
            errors.append(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            errors.append(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            errors.append(
                "Password must contain at least one number."
            )

        if not re.search(r"[@$!%*?&]", value):
            errors.append(
                "Password must contain at least one special character."
            )

        if not re.fullmatch(
            r"[A-Za-z\d@$!%*?&]+",
            value
        ):
            errors.append(
                "Password contains invalid characters."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return value

class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):

        return value.lower().strip()

    def validate(self, attrs):

        email = attrs.get("email")
        otp = attrs.get("otp")

        # Find pending registration
        pending_registration = PendingRegistration.objects.filter(
            email=email
        ).first()

        if not pending_registration:

            raise serializers.ValidationError({
                "email": "Registration not found."
            })

        # Check OTP expiry
        if pending_registration.is_expired():

            raise serializers.ValidationError({
                "otp": "OTP has expired."
            })

        # Check OTP
        if pending_registration.otp != otp:

            raise serializers.ValidationError({
                "otp": "Invalid OTP."
            })

        # Pass pending registration to the view
        attrs["pending_registration"] = pending_registration

        return attrs


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    def validate_email(self, value):

        return value.lower().strip()
    
class ChangePasswordSerializer(serializers.Serializer):
    
    current_password = serializers.CharField(
        write_only = True
    )
    
    new_password = serializers.CharField(
        write_only = True
    )
    
    confirm_password = serializers.CharField(
        write_only = True
    )
    
    def validate_current_password(self, value):
        user = self.context["user"]
        
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Current password is incorrect."
            )
            
        return value 
    
    def validate_new_password(self, value):
        errors = []
        
        if len(value) < 8 or len(value) > 20:
            errors.append(
                "Password must be 8-20 characters long."
            )

        if not re.search(r"[A-Z]", value):
            errors.append(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            errors.append(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            errors.append(
                "Password must contain at least one number."
            )

        if not re.search(r"[@$!%*?&]", value):
            errors.append(
                "Password must contain at least one special character."
            )

        if not re.fullmatch(
            r"[A-Za-z\d@$!%*?&]+",
            value
        ):
            errors.append(
                "Password contains invalid characters."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password":
                    "Passwords do not match."
            })

        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError({
                "new_password":
                    "New password must be different from current password."
            })

        return attrs

    def save(self, **kwargs):

        user = self.context["user"]

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user


class PrivacySettingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PrivacySettings
        fields = [
            "profile_visibility",
            "friend_request_permission",
            "searchable"
        ]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "id",
            "email",
            "phone_number",
            "profile_image",
            "name",
            "bio",
            "date_of_birth",
        ]

        read_only_fields = [
            "id",
            "email",
            "phone_number"
        ]