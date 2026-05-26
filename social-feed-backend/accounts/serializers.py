from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )

        return user
