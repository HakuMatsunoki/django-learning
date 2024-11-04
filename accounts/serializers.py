from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "image_path",
            "created_at",
            "updated_at",
            "is_superuser",
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "image_path",
            "created_at",
        )
