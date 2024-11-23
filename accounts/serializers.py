from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Invite, Request


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


class InviteSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Invite
        fields = ("id", "company", "status", "created_at")


class RequestSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Request
        fields = ("id", "company", "status", "created_at")
