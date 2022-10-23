import base64
from wsgiref.validate import validator

import pyotp
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django_countries.serializers import CountryFieldMixin
from modules.accounts.models import User, Reader
from modules.accounts.tokens import TokenGen
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "email",
            "full_name",
            "role",
            "timestamp",
            "updated_at",
        )
        read_only_fields = ("email", "role")
        extra_kwargs = {
            "phone": {"validators": []},
        }


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )
    password_confirmation = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        style={"input_type": "password confirmation"},
        required=True,
    )
    full_name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = (
            "phone",
            "email",
            "full_name",
            "role",
            "password",
            "password_confirmation",
        )
        read_only_fields = ("role",)

    def create(self, validated_data):
        try:
            user = User.objects.get(
                phone=validated_data["phone"],
            )
            raise serializers.ValidationError(
                "User with this phone number already exists."
            )
        except ObjectDoesNotExist:
            if (
                validated_data["password"]
                and validated_data["password_confirmation"]
                and validated_data["password"]
                == validated_data["password_confirmation"]
            ):
                user = User.objects.create(
                    phone=validated_data["phone"],
                    email=validated_data["email"],
                    full_name=validated_data["full_name"],
                    role="Reader",
                    is_active=False,
                )
                user.set_password(
                    validated_data["password"],
                )
                user.save()
            return user


# Activation Token
class TokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=20)

    class Meta:
        fields = ("token", "phone")


# Request Password Reset Phone where otp will be sent
class RequestPasswordResetPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    class Meta:
        fields = ("phone",)


# Set new Password
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, write_only=True)
    password_confirm = serializers.CharField(max_length=20, write_only=True)
    phone = serializers.CharField(max_length=20)
    token = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        fields = (
            "password",
            "password_confirm",
            "phone",
        )


class ReaderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reader
        fields = (
            "id",
            "user",
            "bio",
            "profile_picture",
            "created_at",
            "updated_at",
        )

        read_only_field = ("id",)

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            user_data = validated_data.pop("user")
            user = instance.user
            user.phone = user_data.get("phone", user.phone)
            user.email = user_data.get("email", user.email)
            user.full_name = user_data.get("full_name", user.full_name)
            user.save()
        # Update profile
        instance.bio = validated_data.get("bio", instance.bio)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.save()

        return instance


class GoogleSocialLoginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=True)

    class Meta:
        fields = ("token",)
