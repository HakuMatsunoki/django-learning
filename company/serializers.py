from rest_framework import serializers

from .models import Company, Invite, Request


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "description",
            "visible",
            "created_at",
            "updated_at",
        )


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
        )


class InviteSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    guest = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Invite
        fields = ("id", "company", "guest", "status", "created_at")


class RequestSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Request
        fields = ("id", "company", "user", "status", "created_at")
