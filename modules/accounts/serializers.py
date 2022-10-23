import base64
from wsgiref.validate import validator

import pyotp
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django_countries.serializers import CountryFieldMixin
from modules.accounts.models import User
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
