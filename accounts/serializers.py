from email.policy import default
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from accounts.models import User


class RegisterUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=127, validators=[
        UniqueValidator(queryset=User.objects.all())])
    birthdate = serializers.DateField()
    bio = serializers.CharField(
        allow_blank=True, allow_null=True, default=None)
    is_critic = serializers.BooleanField(default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    is_superuser = serializers.BooleanField(default=False, read_only=True)

    def create(self, validated_data: dict):
        validated_data['password'] = make_password(validated_data['password'])
        instance = User.objects.create(**validated_data)
        serializer = RegisterUserSerializer(instance)
        return serializer.data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
