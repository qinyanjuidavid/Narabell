import base64

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
