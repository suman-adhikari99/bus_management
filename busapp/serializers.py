from os import access
from unittest.util import _MAX_LENGTH
from .models import Appointment, User, Route, Bus
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', ]
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use'})
        if email == "":
            raise serializers.ValidationError(
                {'email': 'Email is already in use'})
        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=130)
    access = serializers.CharField(max_length=130, read_only=True)
    refresh = serializers.CharField(max_length=120, read_only=True)
